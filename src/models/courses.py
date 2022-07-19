from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin


class Course(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель курса"""

    name = fields.CharField(max_length=255, null=False)
