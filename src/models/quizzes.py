from tortoise import fields
from tortoise.models import Model

from models.base import UUIDModelMixin, AuditMixin


class Quiz(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель теста для домашнего задания"""

    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    answer_type = fields.CharField(max_length=20, null=False)  # single, multi, text
    homework = fields.ForeignKeyField('models.Homework', related_name='quizzes', on_delete='CASCADE')

    additional_files = fields.ManyToManyField('models.File')
    answers: fields.ReverseRelation['Answer']


class Answer(
    UUIDModelMixin, AuditMixin, Model
):
    """Модель ответа на тест"""

    text = fields.TextField(null=False)
    is_correct = fields.BooleanField(default=False)
    quiz = fields.ForeignKeyField('models.Quiz', related_name='answers', on_delete='CASCADE')

    class Meta:
        table = 'quiz_answers'
