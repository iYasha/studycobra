import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from models.base import UUIDModelMixin, AuditMixin, ExpireMixin


class Task(
    UUIDModelMixin, AuditMixin, Base
):
    """ Базовая модель задания """

    __tablename__ = 'tasks'

    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    difficulty = sa.Column(sa.String)


class TaskAnswer(
    UUIDModelMixin, AuditMixin, Base
):
    """ Модель ответа на задание """

    __tablename__ = 'task_answers'

    task_id = sa.Column(UUID, sa.ForeignKey('tasks.id'), nullable=False)
    user_id = sa.Column(UUID, sa.ForeignKey('users.id'), nullable=False)
    answer = sa.Column(sa.String, nullable=False)
    score = sa.Column(sa.Integer)

    task = relationship('Task', back_populates='answers')
