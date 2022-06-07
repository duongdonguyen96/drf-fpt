# from rest_framework import serializers
#
# from core.songs.models import Song
#
#
# class SongBase(serializers.ModelSerializer):
#     name = serializers.CharField(help_text="`name` of song")
#
#     class Meta:
#         model = Song
#         fields = ("id", "name", "albums_id")
#
#
# class SongCreateSerializers(SongBase):
#     albums_id = serializers.IntegerField(help_text="`id` off albums")
#
#
# class SongUpdateSerializers(SongBase):
#     pass
#
#
# class SongResponseSerializers(SongBase):
#     # id = serializers.IntegerField(help_text="`id` of song")
#     pass
