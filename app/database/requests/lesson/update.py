from app.database.models import async_session
from app.database.models import Lesson
from sqlalchemy import update


async def update_lesson_title(id: int, title: str):
    async with async_session() as session:
        await session.execute(update(Lesson).where(Lesson.id == id).values(title=title))
        await session.commit()


async def update_lesson_description(id: int, description: str):
    async with async_session() as session:
        await session.execute(update(Lesson).where(Lesson.id == id).values(description=description))
        await session.commit()


async def update_lesson_video(id: int, video: str):
    async with async_session() as session:
        await session.execute(update(Lesson).where(Lesson.id == id).values(video=video))
        await session.commit()


async def update_lesson_is_free(id: int, is_free: bool):
    async with async_session() as session:
        await session.execute(update(Lesson).where(Lesson.id == id).values(is_free=is_free))
        await session.commit()