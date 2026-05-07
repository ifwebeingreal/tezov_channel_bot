from app.database.models import async_session
from app.database.models import SkateLevel
from sqlalchemy import update


async def update_skate_level(id, name):
    async with async_session() as session:
        await session.execute(update(SkateLevel).where(SkateLevel.id == id).values(name=name))
        await session.commit()