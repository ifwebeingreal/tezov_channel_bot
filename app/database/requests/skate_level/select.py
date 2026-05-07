from app.database.models import async_session
from app.database.models import SkateLevel
from sqlalchemy import select


async def get_skate_levels():
    async with async_session() as session:
        skate_levels = await session.scalars(select(SkateLevel))
        return skate_levels


async def get_skate_level(id):
    async with async_session() as session:
        skate_level = await session.scalar(select(SkateLevel).where(SkateLevel.id == id))
        return skate_level
