from app.database.models import async_session
from app.database.models import Lesson


async def set_lesson(
        title: str, description: str,
        video: str, is_free: bool,
        course_id: int,
):
    async with async_session() as session:
        session.add(Lesson(
            title=title,
            description=description,
            video=video,
            is_free=is_free,
            course_id=course_id
        ))
        await session.commit()