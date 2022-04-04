import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from models.base import UUIDModelMixin, AuditMixin, TrackingMixin


class Session(
    UUIDModelMixin, TrackingMixin, AuditMixin, Base
):
    """ Модель сессии пользователя """

    __tablename__ = 'sessions'

    access_token = sa.Column(sa.String, nullable=True)
    refresh_token = sa.Column(sa.String, nullable=True)
    platform = sa.Column(sa.String, nullable=False)

    user_id = sa.Column(UUID, sa.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='sessions')
