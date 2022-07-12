from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin, TrackingMixin


class Session(
    UUIDModelMixin, TrackingMixin, AuditMixin, Model
):
    """ Модель сессии пользователя """

    access_token = fields.CharField(max_length=255, null=True)
    refresh_token = fields.CharField(max_length=255, null=True)
    platform = fields.CharField(max_length=20)

    user = fields.ForeignKeyField('models.User', related_name='sessions')
