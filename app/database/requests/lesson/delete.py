from app.database.models import async_session
from app.database.models import Lesson
from sqlalchemy import delete


async def delete_lesson(id: int):
    async with async_session() as session:
        await session.execute(delete(Lesson).where(Lesson.id == id))
        await session.commit()