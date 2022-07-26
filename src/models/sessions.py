from tortoise import fields
from tortoise.models import Model

from models.base import UUIDModelMixin, AuditMixin, TrackingMixin


class Session(
    UUIDModelMixin, TrackingMixin, AuditMixin, Model
):
    """ Модель сессии пользователя """

    access_token = fields.TextField(null=True)
    refresh_token = fields.TextField(null=True)
    platform = fields.CharField(max_length=20)

    user = fields.ForeignKeyField('models.User', related_name='sessions')
