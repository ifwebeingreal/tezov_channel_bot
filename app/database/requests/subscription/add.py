from app.database.models import async_session
from app.database.models import Subscription


async def set_subscription(tg_id,
                           start_date,
                           end_date,
                           payment_method_id = None,
                           tariff_id = None,
                           is_active = True):
    async with async_session() as session:
        session.add(Subscription(tg_id=tg_id,
                                 start_date=start_date,
                                 end_date=end_date,
                                 payment_method_id=payment_method_id,
                                 tariff_id=tariff_id,
                                 is_active=is_active))
        await session.commit()