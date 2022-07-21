from typing import List
from uuid import UUID

import enums
import models
import schemas
from core import security


class QuizService:

    @classmethod
    async def create_quizzes(
            cls,
            homework_id: UUID,
            new_quizzes: List[schemas.QuizCreate]
    ) -> List[schemas.Quiz]:
        quizzes = []
        for new_quiz in new_quizzes:
            quiz = await models.Quiz.create(homework_id=homework_id, **new_quiz.dict(exclude={'additional_files', 'answers'}))
            additional_files = await models.File.filter(uuid__in=new_quiz.additional_files)
            await quiz.additional_files.add(*additional_files)
            await quiz.save()

            answers = [models.Answer(quiz=quiz, **x.dict()) for x in new_quiz.answers]
            await models.Answer.bulk_create(answers)

            quizzes.append(schemas.Quiz(
                additional_files=schemas.File.from_queryset(additional_files),
                answers=schemas.Answer.from_queryset(answers),
                **dict(quiz)
            ))
        return quizzes
