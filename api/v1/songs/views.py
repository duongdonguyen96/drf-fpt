from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.v1.songs.serializers import SongResponseSerializers, SongCreateSerializers, SongUpdateSerializers, AlbumSerializer
from core.albums.models import Album
from funtions import message

from funtions.color_text import color
from core.songs.models import Song
from django.db.models import F

from funtions.funtion import nested_list


@api_view(['GET'])
def get_all(request):
    try:
        songs = Song.objects.all()
    except Exception as ex:
        raise APIException(ex)

    serializer = SongResponseSerializers(songs, many=True)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(songs.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(serializer.data)


@api_view(['GET'])
def detail(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    serializer = SongResponseSerializers(song, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def create(request):
    serializer = SongCreateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)  # noqa

    name = serializer.validated_data['name']
    albums_id = serializer.validated_data['albums_id']

    if Song.objects.filter(name=name).exists():
        raise APIException(message.ERROR_NAME_IS_EXISTED)

    try:
        song = Song.objects.create(name=name, albums_id=albums_id)
    except Exception as ex:
        raise APIException(ex)

    return Response({
        "id": song.id,
        "name": song.name,
        "albums_id": albums_id
    })


@api_view(['POST'])
def update(request, song_id):
    serializer = SongUpdateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)  # noqa

    name = serializer.validated_data['name']
    views = serializer.validated_data['views']

    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    song.name = name
    song.views = views

    song.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete(request, song_id):
    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    song.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_top_5_songs_newest(request):
    try:
        songs = Album.objects.all().filter(songs__isnull=False, singers__isnull=False).annotate(
            singer_id=F('singers__id'),
            singer_name=F('singers__name'),
            song_id=F('songs__id'),
            song_name=F('songs__name'),
            album_id=F('id'),
            album_name=F('name'),
        ).values('singer_name', 'album_name', 'song_id', 'song_name').order_by('-song_id')[:5]

    except Exception as ex:
        raise APIException(ex)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(songs.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(songs)


@api_view(['GET'])
def get_top_5_songs(request):
    """
        TOP 5 bài hát mới nhất của albums
    """

    try:
        songs = Album.objects.all().filter(songs__isnull=False, ).annotate(
            song_id=F('songs__id'),
            song_name=F('songs__name'),
            album_id=F('id'),
            album_name=F('name'),
        ).values('song_id', 'song_name', 'album_id', 'album_name').order_by('-song_id')

    except Exception as ex:
        raise APIException(ex)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(songs.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    level_1_data = []
    level_1_ids = []

    for parent in songs:
        if parent['album_id'] in level_1_ids:
            continue
        level_1_data.append({
            "album_id": parent['album_id'],
            "album_name": parent['album_name'],
        })
        level_1_ids.append(parent['album_id'])

    level_2_data = []
    level_2_ids = []

    list_parent_ids = []

    for index, child in enumerate(songs):

        if list_parent_ids.count(child['album_id']) >= 5:
            continue

        if child['album_id'] in level_1_ids:
            level_2_data.append({
                "song_id": child['song_id'],
                "song_name": child['song_name'],
                "parent_uuid": child['album_id']
            })
            level_2_ids.append(child['song_id'])
            list_parent_ids.append(child['album_id'])

    data_res = nested_list(
        level_1_data,
        map_with_key='album_id',
        children_fields={'list_songs': ['song_id', 'song_name']},
        children_list=level_2_data,
        key_child_map_parent='parent_uuid'
    )

    return Response(data_res)
