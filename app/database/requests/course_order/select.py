from app.database.models import async_session
from app.database.models import CourseOrder
from sqlalchemy import select


async def get_course_order(tg_id: int, course_id: int):
    async with async_session() as session:
        result = await session.scalar(
            select(CourseOrder)
            .where(CourseOrder.tg_id==tg_id)
            .where(CourseOrder.course_id==course_id)
        )
        return result
