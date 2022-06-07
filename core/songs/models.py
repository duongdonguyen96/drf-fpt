from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.albums.models import Album
from core.models import BaseModel


class Song(BaseModel):
    name = models.CharField(
        max_length=255, db_column='name', blank=True,
        null=True, verbose_name=_('Name'))

    albums = models.ForeignKey(Album, on_delete=models.RESTRICT, null=True, related_name='songs')

    views = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)],
                                        db_column='views', blank=True, verbose_name=_('Views'))

    class Meta:
        db_table = 'song'
        verbose_name_plural = _('Song')
