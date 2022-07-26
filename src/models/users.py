from tortoise import fields
from tortoise.models import Model

from models.base import UUIDModelMixin, AuditMixin


class User(
    UUIDModelMixin, AuditMixin, Model
):
    """ Базовая модель пользователя """

    name = fields.CharField(max_length=40, null=True)
    email = fields.CharField(max_length=255, unique=True)
    role = fields.CharField(max_length=20)
    hashed_password = fields.CharField(max_length=255, null=True)
    avatar = fields.ForeignKeyField('models.File', null=True, on_delete=fields.SET_NULL)
