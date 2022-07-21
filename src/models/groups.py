from typing import Any

from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin
from models.lessons import Lesson


class Group(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель группы"""

    course = fields.ForeignKeyField('models.Course', related_name='groups')
    start_at = fields.DatetimeField(null=False)
    creator = fields.ForeignKeyField('models.User', related_name='created_groups', on_delete='CASCADE')
    is_archived = fields.BooleanField(default=False)

    lessons: fields.ReverseRelation['Lesson']
    students: fields.ReverseRelation['GroupStudent']
    teachers: fields.ReverseRelation['GroupTeacher']


class GroupStudent(UUIDModelMixin, Model):
    """Модель связи группы и ученика"""

    group = fields.ForeignKeyField('models.Group', related_name='students', on_delete='CASCADE')
    user = fields.ForeignKeyField('models.User', related_name='students', on_delete='CASCADE')
    is_archived = fields.BooleanField(default=False)

    class Meta:
        table = 'group_student'


class GroupTeacher(UUIDModelMixin, Model):
    user = fields.ForeignKeyField('models.User', related_name='teachers', on_delete='CASCADE')
    group = fields.ForeignKeyField('models.Group', related_name='teachers', on_delete='CASCADE')
    role = fields.CharField(max_length=20)

    class Meta:
        table = 'group_teacher'
