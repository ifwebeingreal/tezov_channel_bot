from app.database.models import async_session
from app.database.models import Figure


async def set_figure(name, level_id):
    async with async_session() as session:
        session.add(Figure(name=name, level_id=level_id))
        await session.commit()