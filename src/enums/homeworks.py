from enum import Enum


class DifficultyLevel(int, Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class HomeworkType(str, Enum):
    DEFAULT = 'default'
    QUIZ = 'quiz'
