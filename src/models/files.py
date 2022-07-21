from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin


class File(
    UUIDModelMixin, AuditMixin, Model
):
    """ Модель хранения файлов """

    name = fields.CharField(max_length=255, null=False)
    content_type = fields.CharField(max_length=255, null=False)
    size = fields.FloatField(null=False)
