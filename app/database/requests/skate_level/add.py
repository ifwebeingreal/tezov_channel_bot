from app.database.models import async_session
from app.database.models import SkateLevel


async def set_skate_level(name):
    async with async_session() as session:
        session.add(SkateLevel(name=name))
        await session.commit()