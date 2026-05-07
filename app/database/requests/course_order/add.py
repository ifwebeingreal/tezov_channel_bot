from app.database.models import async_session
from app.database.models import CourseOrder


async def set_course_order(tg_id: int, course_id: int):
    async with async_session() as session:
        session.add(CourseOrder(course_id=course_id, tg_id=tg_id))
        await session.commit()