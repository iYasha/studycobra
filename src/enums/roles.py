from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    SUPPORT = 'support'


class TeacherRole(str, Enum):
    COACH = 'coach'
    MENTOR = 'mentor'
    VISITOR = 'visitor'

