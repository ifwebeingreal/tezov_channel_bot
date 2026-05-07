from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import update


async def update_subscription_end_date(tg_id, end_date, tariff_id, payment_method_id = None):
    async with async_session() as session:
        await session.execute(
            update(Subscription).where(Subscription.tg_id == tg_id).values(
                end_date=end_date,
                tariff_id=tariff_id,
                payment_method_id=payment_method_id
            )
        )
        await session.commit()


async def update_subscription_is_active(tg_id, is_active):
    async with async_session() as session:
        await session.execute(
            update(Subscription).where(Subscription.tg_id == tg_id).values(
                is_active=is_active
            )
        )
        await session.commit()