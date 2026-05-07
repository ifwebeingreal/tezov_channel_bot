from app.database.models import async_session
from app.database.models import SkateLevel
from sqlalchemy import delete


async def delete_skate_level(id):
    async with async_session() as session:
        await session.execute(delete(SkateLevel).where(SkateLevel.id == id))
        await session.commit()