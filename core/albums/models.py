from core.models import BaseModel
from django.db import models

from django.utils.translation import ugettext_lazy as _

from core.singer.models import Singer


class Album(BaseModel):
    name = models.CharField(
        max_length=255, db_column='name', blank=True,
        null=True, verbose_name=_('Name'))

    singers = models.ForeignKey(Singer, on_delete=models.CASCADE, null=True, related_name='albums')

    class Meta:
        db_table = 'album'
        verbose_name_plural = _('Album')
