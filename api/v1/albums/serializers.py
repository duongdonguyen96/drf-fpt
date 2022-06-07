from rest_framework import serializers

from core.albums.models import Album


class AlbumBase(serializers.ModelSerializer):
    name = serializers.CharField(help_text="`name` of album")

    class Meta:
        model = Album
        fields = ("id", "name", "singers_id")


class AlbumCreateSerializers(AlbumBase):
    singers_id = serializers.IntegerField(help_text="`id` off singer")


class AlbumUpdateSerializers(AlbumBase):
    pass
    # singers_id = serializers.IntegerField(help_text="`id` off singer")


class AlbumResponseSerializers(AlbumBase):
    pass

#
# class Top10AlbumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Album
#         fields = ("id", "name", "singers_id", "singer.name")
