from app.database.models import async_session
from app.database.models import Trick


async def set_trick(name, description, video, figure_id, level_id, price):
    async with async_session() as session:
        session.add(Trick(name=name,
                          description=description,
                          video=video,
                          figure_id=figure_id,
                          level_id=level_id,
                          price=price))
        await session.commit()