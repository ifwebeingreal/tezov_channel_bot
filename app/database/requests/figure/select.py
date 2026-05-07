from app.database.models import async_session
from app.database.models import Figure
from sqlalchemy import select


async def get_figures():
    async with async_session() as session:
        figures = await session.scalars(select(Figure))
        return figures


async def get_figure(id):
    async with async_session() as session:
        figure = await session.scalar(select(Figure).where(Figure.id == id))
        return figure


async def get_figures_by_level_id(level_id):
    async with async_session() as session:
        figures = await session.scalars(select(Figure).where(Figure.level_id == level_id))
        return figures.all()
