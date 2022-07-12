from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin, ExpireMixin


class User(
    UUIDModelMixin, AuditMixin, Model
):
    """ Базовая модель пользователя """

    name = fields.CharField(max_length=40, null=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255, null=True)
