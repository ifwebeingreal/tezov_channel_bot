from app.database.models import async_session
from app.database.models import Trick
from sqlalchemy import update


async def update_trick_name(id, name):
    async with async_session() as session:
        await session.execute(update(Trick).where(Trick.id == id).values(name=name))
        await session.commit()


async def update_trick_video(id, video):
    async with async_session() as session:
        await session.execute(update(Trick).where(Trick.id == id).values(video=video))
        await session.commit()


async def update_trick_description(id, description):
    async with async_session() as session:
        await session.execute(update(Trick).where(Trick.id == id).values(description=description))
        await session.commit()


async def update_trick_price(id, price):
    async with async_session() as session:
        await session.execute(update(Trick).where(Trick.id == id).values(price=price))
        await session.commit()