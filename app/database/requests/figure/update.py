from app.database.models import async_session
from app.database.models import Figure
from sqlalchemy import update


async def update_figure_name(id, name):
    async with async_session() as session:
        await session.execute(update(Figure).where(Figure.id == id).values(name=name))
        await session.commit()