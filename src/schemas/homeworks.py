from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import validator, Field

import enums
from schemas.base import UUIDSchemaMixin, QuerySetMixin, BaseSchema
from schemas.files import File
from schemas.groups import GroupTeacher
from schemas.quizzes import Quiz, QuizCreate
from schemas.users import User


class HomeworkBase(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    time_terms: datetime
    retakes_count: int
    difficulty_level: enums.DifficultyLevel
    homework_type: enums.HomeworkType
    overdue_pass: bool = False

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class Homework(UUIDSchemaMixin, QuerySetMixin, HomeworkBase):
    author: Optional[GroupTeacher] = None
    quizzes: List[Quiz] = Field(default_factory=list)
    additional_files: List[File] = Field(default_factory=list, description='Id\'s of File instance')


class HomeworkCreate(HomeworkBase):
    quizzes: List[QuizCreate] = Field(default_factory=list)
    author_id: Optional[UUID] = Field(
        default=None,
        description='Id of GroupTeacher instance that will be check this homework'
    )
    additional_files: List[UUID] = Field(default_factory=list, description='Id\'s of File instance')


class HomeworkAnswer(UUIDSchemaMixin, QuerySetMixin, BaseSchema):
    answer: Optional[str] = None
    teacher_description: Optional[str] = None
    points: Optional[int] = None
    file: Optional[File] = None
    teacher_file: Optional[File] = None
    student: User

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class HomeworkAnswerStudentCreate(BaseSchema):
    answer: Optional[str] = None
    file_id: Optional[UUID] = None

    @validator('*', pre=True)
    def validate_answer(cls, v, values, **kwargs):
        if values['answer'] is None and values['file_id'] is None:
            raise ValueError('Answer or file_id must be set')
        return v


class HomeworkAnswerTeacherCreate(BaseSchema):
    teacher_description: Optional[str] = None
    teacher_file_id: Optional[UUID] = None
    points: int = Field(ge=0, le=100)

    @validator('*', pre=True)
    def validate_teacher_description(cls, v, values, **kwargs):
        if values['teacher_description'] is None and values['teacher_file_id'] is None:
            raise ValueError('Teacher_description or teacher_file_id must be set')
        return v

