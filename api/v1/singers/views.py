from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.v1.singers.serializers import SingerResponseSerializers, SingerCreateSerializers, SingerUpdateSerializers
from core.albums.models import Album
from funtions import message
from funtions.color_text import color
from core.singer.models import Singer
from django.db.models import F
from django.db import connection

from funtions.funtion import dict_fetchall


@api_view(['GET'])
def get_all(request):
    try:
        singers = Singer.objects.all()
    except Exception as ex:
        raise APIException(ex)

    serializer = SingerResponseSerializers(singers, many=True)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(singers.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(serializer.data)


@api_view(['GET'])
def detail(request, singer_id):
    try:
        singer = Singer.objects.get(id=singer_id)
    except Singer.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    serializer = SingerResponseSerializers(singer, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def create(request):
    serializer = SingerCreateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    name = serializer.validated_data['name']
    stage_name = serializer.validated_data['stage_name']
    birthday = serializer.validated_data['birthday']
    address = serializer.validated_data['address']

    if Singer.objects.filter(stage_name=stage_name).exists():
        raise APIException(message.ERROR_STAGE_NAME_IS_EXISTED)

    try:
        singer = Singer.objects.create(name=name, stage_name=stage_name, birthday=birthday, address=address)
    except Exception as ex:
        raise APIException(ex)

    return Response({
        "id": singer.id,
        "name": singer.name,
        "stage_name": singer.stage_name,
        "birthday": singer.birthday,
        "address": singer.address,
        "created_at": singer.created_at,
        "updated_at": singer.created_at,
    })


@api_view(['POST'])
def update(request, singer_id):
    serializer = SingerUpdateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)

    name = serializer.validated_data['name']
    stage_name = serializer.validated_data['stage_name']
    birthday = serializer.validated_data['birthday']
    address = serializer.validated_data['address']

    try:
        singer = Singer.objects.get(id=singer_id)
    except Singer.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    singer.name = name
    singer.stage_name = stage_name
    singer.birthday = birthday
    singer.address = address

    singer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete(request, singer_id):
    try:
        singer = Singer.objects.get(id=singer_id)
    except Singer.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    singer.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_list_albums(request, singer_id):
    """
    Lấy danh sách album của 1 ca sĩ
    """
    try:
        data = Album.objects.all().filter(singers__id=singer_id).annotate(
            singer_name=F('singers__name'),
            singer_id=F('singers__id'),
            album_name=F('name')
        ).order_by('-id').values('album_name', 'singer_name', 'singer_id')

    except Exception as ex:
        raise APIException(ex)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(data.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(data)


@api_view(['GET'])
def get_list_songs(request, singer_id):
    """
    Lấy danh sách bài hát của 1 ca sĩ
    """
    # TODO prefetch_related
    # response = Singer.objects.prefetch_related('album_set').all()
    # ModelA.objects.prefetch_related('modelb_set').all()

    sql = """SELECT SONG.ID AS song_id,SONG.NAME as song_name,SINGER.ID,SINGER.NAME  FROM SINGER
            INNER JOIN ALBUM ON ("ALBUM"."SINGERS_ID" = "SINGER"."ID")
            INNER JOIN SONG ON ("SONG"."ALBUMS_ID" = "ALBUM"."ID")
            WHERE SINGER.ID =%s""" % singer_id

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = dict_fetchall(cursor)
    except Exception as ex:
        raise APIException(ex)

    return Response(data)


@api_view(['POST'])
def search_data(request):
    """
    Tìm kiếm bài hát, album, ca sĩ theo data truyền vào
     input: data
     output:
     {
        songs:[],
        albums:[],
        singers:[]
    }
    """
    data_search = request.data.get('data')
    if not data_search:
        raise APIException(message.DATA_IS_NOT_NONE)

    try:
        singers = Singer.objects.all().filter(name__icontains=data_search).values('id', 'name')[:5]

        albums = Album.objects.all().filter(name__icontains=data_search).select_related('singers').annotate(
            album_name=F('name'),
            singer_name=F('singers__name'),
            singer_id=F('singers__id'),
        ).values('album_name', 'singer_name', 'singer_id')[:5]

        songs = Album.objects.all().filter(songs__name__icontains=data_search).select_related('singers').annotate(
            singer_id=F('singers__id'),
            singer_name=F('singers__name'),
            song_id=F('songs__id'),
            song_name=F('songs__name'),
        ).values('singer_id', 'singer_name', 'song_id', 'song_name')[:5]

    except Exception as ex:
        raise APIException(ex)

    print(color.OKGREEN + "-------------------SINGER-----------------" + color.ENDC)
    print(singers.query)
    print(color.WARNING + "-------------------ALBUM------------------" + color.ENDC)
    print(albums.query)
    print(color.OKBLUE + "--------------------SONG-------------------" + color.ENDC)
    print(songs.query)

    return Response(
        {'songs': songs,
         "albums": albums,
         "singers": singers
         })
