from datetime import datetime

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

    def can_be_created(self, student_retakes_count: int) -> bool:
        is_not_overdue = (self.time_terms > datetime.now() and not self.overdue_pass) or self.overdue_pass
        has_retakes_count = self.retakes_count > student_retakes_count
        return is_not_overdue and has_retakes_count


class HomeworkAnswer(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель решения домашнего задания"""

    answer = fields.TextField(null=True)
    teacher_description = fields.TextField(null=True)
    points = fields.IntField(null=True)

    student = fields.ForeignKeyField('models.User', related_name='homework_answers', on_delete='CASCADE')
    file = fields.ForeignKeyField('models.File', null=True, related_name='homework_answers_student_files', on_delete=fields.SET_NULL)
    teacher_file = fields.ForeignKeyField('models.File', related_name='homework_answers_teacher_files', null=True, on_delete=fields.SET_NULL)
    homework = fields.ForeignKeyField('models.Homework', related_name='answers', on_delete='CASCADE')




