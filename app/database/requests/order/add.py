from app.database.models import async_session
from app.database.models import Order


async def set_order(user_id, trick_id):
    async with async_session() as session:
        order = Order(user_id=user_id,
                      trick_id=trick_id)
        session.add(order)
        await session.commit()