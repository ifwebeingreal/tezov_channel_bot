from app.database.models import async_session
from app.database.models import Order
from sqlalchemy import select


async def get_order(user_id: int, trick_id: int):
    async with async_session() as session:
        order = await session.scalar(
            select(Order).where(Order.user_id == user_id, Order.trick_id == trick_id)
        )
        return order