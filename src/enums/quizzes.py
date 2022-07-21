from enum import Enum


class AnswerType(str, Enum):
    SINGLE = 'single'
    MULTI = 'multi'
    TEXT = 'text'
