from typing import Optional, List
from uuid import UUID

from pydantic import Field

import enums
from schemas.base import UUIDSchemaMixin, QuerySetMixin, BaseSchema
from schemas.files import File


class QuizBase(BaseSchema):
    title: str
    description: Optional[str] = None
    answer_type: enums.AnswerType

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class Answer(QuerySetMixin, BaseSchema):
    text: str
    is_correct: bool

    class Config:
        orm_mode = True


class Quiz(UUIDSchemaMixin, QuerySetMixin, QuizBase):
    additional_files: List[File] = Field(default_factory=list, description='Id\'s of File instance')
    answers: List[Answer] = Field(default_factory=list, description='Id\'s of Answer instance')


class QuizCreate(QuizBase):
    additional_files: List[UUID] = Field(default_factory=list, description='Id\'s of File instance')
    answers: List[Answer]
