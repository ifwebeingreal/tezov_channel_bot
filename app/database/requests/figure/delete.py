from app.database.models import async_session
from app.database.models import Figure
from sqlalchemy import delete


async def delete_figure(id):
    async with async_session() as session:
        await session.execute(delete(Figure).where(Figure.id == id))
        await session.commit()