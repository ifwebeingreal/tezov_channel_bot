from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import delete


async def delete_subscription(id):
    async with async_session() as session:
        await session.execute(delete(Subscription).where(Subscription.id == id))
        await session.commit()


async def delete_subscription_by_tg_id(tg_id):
    async with async_session() as session:
        await session.execute(delete(Subscription).where(Subscription.tg_id == tg_id))
        await session.commit()