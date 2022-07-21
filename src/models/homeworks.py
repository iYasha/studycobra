from tortoise.models import Model
from tortoise import fields

from models.base import UUIDModelMixin, AuditMixin
from models.quizzes import Quiz


class Homework(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель домашнего задания"""

    title = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    time_terms = fields.DatetimeField(null=False)
    retakes_count = fields.IntField(null=False)
    difficulty_level = fields.IntField(null=False)
    overdue_pass = fields.BooleanField(default=False)
    homework_type = fields.CharField(max_length=20, null=False)  # default, quiz

    lesson = fields.ForeignKeyField('models.Lesson', related_name='homeworks', on_delete='CASCADE')
    author = fields.ForeignKeyField('models.GroupTeacher', null=True, related_name='homeworks', on_delete=fields.SET_NULL)

    additional_files = fields.ManyToManyField('models.File')

    quizzes: fields.ReverseRelation['Quiz']

