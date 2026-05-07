from app.database.models import async_session
from app.database.models import Course


async def set_course(title: str, price: float,
                     description: str, video: str):
    async with async_session() as session:
        course = Course(title=title,
                        price=price,
                        description=description,
                        video=video)
        session.add(course)
        await session.commit()