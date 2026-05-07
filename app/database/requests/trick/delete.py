from app.database.models import async_session
from app.database.models import Trick
from sqlalchemy import delete


async def delete_trick(id):
    async with async_session() as session:
        await session.execute(delete(Trick).where(Trick.id == id))
        await session.commit()