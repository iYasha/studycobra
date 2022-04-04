import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from models.base import UUIDModelMixin, AuditMixin, ExpireMixin


class User(
    UUIDModelMixin, AuditMixin, Base
):
    """ Базовая модель пользователя """

    __tablename__ = 'users'

    name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=False, unique=True)
    hashed_password = sa.Column(sa.String, nullable=True)

    is_superuser = sa.Column(sa.Boolean, default=False)

