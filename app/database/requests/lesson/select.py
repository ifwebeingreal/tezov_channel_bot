from app.database.models import async_session
from app.database.models import Lesson
from sqlalchemy import select


async def get_lessons_by_course_id(course_id: int):
    async with async_session() as session:
        lessons = await session.scalars(select(Lesson).where(Lesson.course_id == course_id))
        return lessons


async def get_lesson(id: int):
    async with async_session() as session:
        lesson = await session.scalar(select(Lesson).where(Lesson.id == id))
        return lesson


async def get_free_lessons(course_id: int):
    async with async_session() as session:
        lesson = await session.scalars(
            select(Lesson)
            .where(Lesson.course_id == course_id)
            .where(Lesson.is_free == True)
        )
        return lesson


async def get_not_free_lessons(course_id: int):
    async with async_session() as session:
        lesson = await session.scalars(
            select(Lesson)
            .where(Lesson.course_id == course_id)
            .where(Lesson.is_free == False)
        )
        return lesson