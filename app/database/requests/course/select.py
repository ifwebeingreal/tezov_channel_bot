from app.database.models import async_session
from app.database.models import Course
from sqlalchemy import select


async def get_courses():
    async with async_session() as session:
        courses = await session.scalars(select(Course))
        return courses


async def get_course(id: int):
    async with async_session() as session:
        course = await session.scalar(select(Course).where(Course.id == id))
        return course