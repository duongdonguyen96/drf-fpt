from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.v1.albums.serializers import AlbumResponseSerializers, AlbumCreateSerializers, AlbumUpdateSerializers
from core.singer.models import Singer
from funtions import message
from core.albums.models import Album
from funtions.color_text import color

from django.db.models import F


@api_view(['GET'])
def get_all(request):
    try:
        albums = Album.objects.all()
    except Exception as ex:
        raise APIException(ex)

    serializer = AlbumResponseSerializers(albums, many=True)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(albums.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(serializer.data)


@api_view(['GET'])
def detail(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    serializer = AlbumResponseSerializers(album, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def create(request):
    serializer = AlbumCreateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)  # noqa

    name = serializer.validated_data['name']
    singers_id = serializer.validated_data['singers_id']

    if Album.objects.filter(name=name).exists():
        raise APIException(message.ERROR_NAME_IS_EXISTED)

    try:
        album = Album.objects.create(name=name, singers_id=singers_id)
    except Exception as ex:
        raise APIException(ex)

    return Response({
        "id": album.id,
        "name": album.name,
        "singers_id": album.singers_id
    })


@api_view(['POST'])
def update(request, album_id):
    serializer = AlbumUpdateSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)  # noqa

    name = serializer.validated_data['name']
    # singers_id = serializer.validated_data['singers_id']

    if Album.objects.filter(name=name).exists():
        raise APIException(message.ERROR_NAME_IS_EXISTED)

    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    album.name = name
    # album.singers_id = singers_id

    album.save()

    return Response(serializer.data)


@api_view(['DELETE'])  # noqa
def delete(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    album.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_top_10_albums(request):
    """
        Lấy 10 album mới nhất
    """
    try:
        data = Album.objects.all().select_related('singers').annotate(
            singer_name=F('singers__name')).order_by('-id')[:10].values('id', 'name', 'singer_name')

    except Exception as ex:
        raise APIException(ex)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(data.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(data)


@api_view(['GET'])
def get_albums_of_singer(request):
    """
        Lấy tất cả album của ca sĩ
    """
    try:
        data = Singer.objects.all().prefetch_related('albums').annotate(
            singer_name=F('name'),
            singer_id=F('id'),
            album_id=F('albums__id'),
            album_name=F('albums__name'),
        ).values('singer_id', 'singer_name', 'album_id', 'album_name')

    except Exception as ex:
        raise APIException(ex)

    print(color.WARNING + "-------------------RAW SQL-----------------" + color.ENDC)
    print(data.query)
    print(color.WARNING + "-------------------------------------------" + color.ENDC)

    return Response(data)
