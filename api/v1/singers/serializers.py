from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core.singer.models import Singer


class SingerBase(serializers.ModelSerializer):
    name = serializers.CharField(help_text="`name` of singer")
    stage_name = serializers.CharField(help_text="`stage_name` of singer")
    birthday = serializers.DateField(help_text="`birthday` of singer")
    address = serializers.CharField(help_text="`address` of singer")


class SingerCreateSerializers(SingerBase):
    class Meta:
        model = Singer
        fields = ('name', 'stage_name', 'birthday', 'address')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('name', 'stage_name'),
                message=_("Test unique together"))
        ]


class SingerUpdateSerializers(SingerBase):
    class Meta:
        model = Singer
        fields = ('name', 'stage_name', 'birthday', 'address')


class SingerResponseSerializers(SingerBase):
    id = serializers.IntegerField(help_text="`id` of singer")
    created_at = serializers.DateTimeField(help_text="`created_at`")
    updated_at = serializers.DateTimeField(help_text="`updated_at`")

    class Meta:
        model = Singer
        fields = "__all__"
