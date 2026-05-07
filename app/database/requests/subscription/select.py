from datetime import datetime

from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import select


async def get_subscriptions():
    async with async_session() as session:
        subscriptions = await session.scalars(select(Subscription))
        return subscriptions


async def get_subscription(tg_id):
    async with async_session() as session:
        subscription = await session.scalar(select(Subscription).where(Subscription.tg_id == tg_id))
        return subscription


async def get_expired_subscriptions():
    async with async_session() as session:
        result = await session.execute(select(Subscription).where(Subscription.end_date <= datetime.now()))
        subscriptions = result.scalars().all()
        return subscriptions