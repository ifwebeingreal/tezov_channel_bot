from app.database.models import async_session
from app.database.models import Course
from sqlalchemy import delete


async def delete_course(id: int):
    async with async_session() as session:
        await session.execute(delete(Course).where(Course.id == id))
        await session.commit()