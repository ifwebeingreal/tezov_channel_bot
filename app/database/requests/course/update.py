from app.database.models import async_session
from app.database.models import Course
from sqlalchemy import update


async def update_course_title(id: int, title: str):
    async with async_session() as session:
        await session.execute(update(Course).where(Course.id == id).values(title=title))
        await session.commit()


async def update_course_price(id: int, price: float):
    async with async_session() as session:
        await session.execute(update(Course).where(Course.id == id).values(price=price))
        await session.commit()


async def update_course_description(id: int, description: str):
    async with async_session() as session:
        await session.execute(update(Course).where(Course.id == id).values(description=description))
        await session.commit()


async def update_course_video(id: int, video: str):
    async with async_session() as session:
        await session.execute(update(Course).where(Course.id == id).values(video=video))
        await session.commit()