from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import BaseModel


class Singer(BaseModel):
    name = models.CharField(
        max_length=255, db_column='name', verbose_name=_('Name'))

    stage_name = models.CharField(
        max_length=255, db_column='stage_name', blank=True,
        null=True, )

    birthday = models.DateField(db_column='birthday', blank=True, null=True)

    address = models.CharField(
        max_length=200, db_column='address', blank=True,
        null=True, verbose_name=_('Address'))

    class Meta:
        db_table = 'singer'
        verbose_name_plural = _('Singer')
