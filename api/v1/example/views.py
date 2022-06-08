from django.db.models import Case
from django.db.models import CharField
from django.db.models import Count
from django.db.models import F
from django.db.models import Max
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models import Value
from django.db.models import When
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from core.albums.models import Album
from core.songs.models import Song
from funtions.color_text import color
from funtions.funtion import query_debugger


@api_view(["GET"])
def greate_than(request):
    try:
        songs = list(Song.objects.filter(id__gte=1).values("id", "name"))
    except Song.DoesNotExist as ex:
        raise APIException(ex)
    except Exception as ex:
        raise APIException(ex)

    return Response(songs)


@api_view(["GET"])
def q_object(request):
    try:
        songs = (Song.objects.all()
                 .filter(Q(name__icontains="y"), Q(id=1) | Q(id__gt=1))
                 .values("id", "name"))
    except Exception as ex:
        raise APIException(ex)

    print(color.OKGREEN + "------------------- SQL -----------------" +
          color.ENDC)
    print(songs.query)

    return Response(list(songs.values("id", "name")))


@api_view(["GET"])
def sub_query(request):
    try:
        album_sub_query = Album.objects.only("id").all()
        songs = (Song.objects.values().filter(
            albums_id__in=album_sub_query).order_by("-id"))
        print(songs.query)

    except Exception as ex:
        raise APIException(ex)

    print(color.OKGREEN + "------------------- SQL -----------------" +
          color.ENDC)
    print(songs.query)

    return Response(songs)


@api_view(["GET"])
@query_debugger
def sub_query_limit(request):
    """
    Trả ra tất cả albums và 5 bài hát mới nhất của album đó
               [
                    {
                        "album_id": 1,
                        "album_name": "Xin đừng lặng im",
                        "top5_songs": [
                            {
                                "song_id": 1,
                                "song_name": "Xin đừng lặng im 1"
                            },...
                        ]
                    },...
                ]
    """

    try:
        albums = (Album.objects.filter(songs__id__in=Subquery(
            Song.objects.filter(albums_id=OuterRef("pk")).order_by("-id")[:5]
            .values_list("id", flat=True))).annotate(
                album_id=F("id"),
                album_name=F("name"),
                song_id=F("songs__id"),
                song_name=F("songs__name"), )
                  .values("album_id", "album_name", "song_id", "song_name"))

        print(color.OKGREEN + "------------------- SQL -----------------" +
              color.ENDC)
        print(albums.query)

        data = list(
            albums.values("album_id", "album_name", "song_id", "song_name"))

    except Exception as ex:
        raise APIException(ex)

    # albums = list(Album.objects.all().prefetch_related('songs'))
    #
    # albums_res = []
    # for album in albums:
    #     songs = [
    #         {
    #             "song_name": song.name,
    #             "song_id": song.id
    #         } for song in album.songs.all().order_by('-id')[:5]
    #     ]
    #
    #     albums_res.append({'name': album.name, 'songs': songs})

    return Response(data)


@api_view(["GET"])
@query_debugger
def count(request):
    """
    Lấy tổng số bài hát của albums

    response:
        [
            {
                "id": 1,
                "name": "Những kẻ mộng mơ1",
                "total_songs": 3
            },
            {
                "id": 3,
                "name": "Xin đừng lặng im",
                "total_songs": 8
            }
        ]

    """
    try:
        album = (Album.objects.values("id")
                 .annotate(total_songs=Count("songs__id"))
                 .values("id", "name", "total_songs"))

        # album = Album.objects.annotate(
        # total_songs=SubqueryCount('songs__id')).values(
        #     'id',
        #     'name',
        #     'total_songs'
        # )

        print(color.OKGREEN + "------------------- SQL -----------------" +
              color.ENDC)
        print(album.query)
    except Exception as ex:
        raise APIException(ex)

    return Response(album)


@api_view(["GET"])
def aggregate(request):
    try:
        aggr = Song.objects.all().aggregate(
            sum_views=Sum("views"),
            max_views=Max("views"),
            min_views=Min("views"))
    except Exception as ex:
        raise APIException(ex)

    return Response(aggr)


@api_view(["GET"])
def when_then(request):
    try:
        rank_of_song = Song.objects.annotate(rank=Case(
            When(views__lte=10, then=Value("F")),
            When(views__gt=10, then=Value("A")),
            default=Value("No rank"),
            output_field=CharField(), )).values("id", "name", "views", "rank")
    except Exception as ex:
        raise APIException(ex)
    print("_____________")
    print(rank_of_song.query)
    rank_of_song = list(rank_of_song.values("id", "name", "views", "rank"))

    return Response(rank_of_song)


@api_view(["GET"])
def f(request):
    try:
        song = Song.objects.get(id=4)
    except Exception as ex:
        raise APIException(ex)

    song.views = F("views") + 3
    song.save()
    print(song.views)
    song.refresh_from_db()

    Song.objects.update(views=F("views") + 2)

    return Response({
        "id": song.id,
        "name": song.name,
        "views": song.views,
    })


# @api_view(['GET'])
# def get_all(request):
#     songs = Song.objects.filter(albums=OuterRef('pk')).only('pk')
#     data = Album.objects.annotate(song=Subquery(songs.values('id')[:1]))
#     print(data.query)
#     data = list(data.values())
#
#     print(type(data))
#     return JsonResponse(data, safe=False)

# try:
#     songs = Song.objects.all()
# except Exception as ex:
#     raise APIException(ex)
#
# serializer = SongResponseSerializers(songs, many=True)
#
# print(color.WARNING + "---------RAW SQL----------" + color.ENDC)
# print(songs.query)
# print(color.WARNING + "-----------" + color.ENDC)

# albums = Album.objects.filter(songs__in=Song.objects.order_by('-id')[:5])

# songs = Song.objects.order_by('-id')[:5]
# albums = Album.objects.filter(songs__in=songs)
