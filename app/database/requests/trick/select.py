from app.database.models import async_session
from app.database.models import Trick
from sqlalchemy import select, func


async def get_tricks():
    async with async_session() as session:
        tricks = await session.scalars(select(Trick))
        return tricks


async def get_trick_by_id(id):
    async with async_session() as session:
        tricks = await session.scalar(select(Trick).where(Trick.id == id))
        return tricks


async def get_tricks_by_level_id_and_figure_id(level_id, figure_id):
    async with async_session() as session:
        tricks = await session.scalars(
            select(Trick).where(Trick.level_id == level_id).where(Trick.figure_id == figure_id)
        )
        return tricks.all()


async def search_tricks_by_name(query: str, level_id: int, figure_id: int):
    async with async_session() as session:
        stmt = (
            select(Trick)
            .where(Trick.name.collate("NOCASE").like(f"%{query}%"))
            .where(Trick.level_id == level_id)
            .where(Trick.figure_id == figure_id)
        )

        print("🧩 SQL:", stmt)
        result = await session.execute(stmt)
        tricks = result.scalars().all()
        print(f"✅ Найдено трюков: {len(tricks)}")
        return tricks