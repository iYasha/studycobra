import enums
import models
import schemas


class GroupService:

    @classmethod
    async def create_group(
            cls,
            creator: models.User,
            new_group: schemas.GroupCreate
    ) -> schemas.Group:
        group_data = new_group.dict()
        teachers = group_data.pop('teachers')
        students = group_data.pop('students')

        group = await models.Group.create(**group_data, creator=creator)
        await group.save()
        await models.GroupTeacher.bulk_create(
            [models.GroupTeacher(user_id=x, role=enums.TeacherRole.COACH.value, group=group) for x in teachers]
        )
        await models.GroupStudent.bulk_create([models.GroupStudent(user_id=x, group=group) for x in students])
        course = await group.course.get()
        return schemas.Group(
            **dict(group),
            course=dict(course),
            teachers=schemas.GroupTeacher.from_queryset(
                await models.GroupTeacher.filter(group=group).all().select_related('user')
            ),
            students=students,
        )
