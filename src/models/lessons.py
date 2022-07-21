from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin
from models.homeworks import Homework


class Lesson(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель занятия"""

    title = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    start_at = fields.DatetimeField(null=False)
    end_at = fields.DatetimeField(null=False)
    group = fields.ForeignKeyField('models.Group', related_name='lessons', on_delete='CASCADE')
    teachers = fields.ManyToManyField('models.GroupTeacher', related_name='lessons')

    additional_files = fields.ManyToManyField('models.File')

    homeworks: fields.ReverseRelation['Homework']

