from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from core.albums.models import Album
from core.songs.models import Song


class SongBase(serializers.ModelSerializer):
    name = serializers.CharField(help_text="`name` of song")

    class Meta:
        model = Song
        fields = ("id", "name", "albums_id", 'views')


class SongCreateSerializers(SongBase):
    albums_id = serializers.IntegerField(help_text="`id` off song")


class SongUpdateSerializers(SongBase):
    views = serializers.IntegerField(help_text="`views` of song")
    pass


class SongResponseSerializers(SongBase):
    # id = serializers.IntegerField(help_text="`id` of song")
    pass


class SongListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    list_song = SongListSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'
