from app.database.models import async_session
from app.database.models import Tariff
from sqlalchemy import update


async def update_tariff_nane(id, name):
    async with async_session() as session:
        await session.execute(update(Tariff).where(Tariff.id == id).values(name=name))
        await session.commit()


async def update_tariff_price(id, price):
    async with async_session() as session:
        await session.execute(update(Tariff).where(Tariff.id == id).values(price=price))
        await session.commit()


async def update_tariff_days_count(id, days_count):
    async with async_session() as session:
        await session.execute(update(Tariff).where(Tariff.id == id).values(days_count=days_count))
        await session.commit()