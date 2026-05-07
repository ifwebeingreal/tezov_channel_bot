from app.database.models import async_session
from app.database.models import Tariff


async def set_tariff(name, price, days_count):
    async with async_session() as session:
        session.add(Tariff(name=name,
                           price=price,
                           days_count=days_count))
        await session.commit()