from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=config.database.sqlalchemy_url(),
                             echo=False)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    date: Mapped[str]


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)


class Tariff(Base):
    __tablename__ = 'tariffs'

    id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[float]
    days_count: Mapped[int]


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    start_date: Mapped[str]
    end_date: Mapped[str]
    payment_method_id: Mapped[str] = mapped_column(nullable=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey('tariffs.id'))
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)


class SkateLevel(Base):
    __tablename__ = 'skate_level'

    id: Mapped[intpk]
    name: Mapped[str]


class Figure(Base):
    __tablename__ = 'figure'

    id: Mapped[intpk]
    name: Mapped[str]
    level_id: Mapped[int] = mapped_column(ForeignKey('skate_level.id'))


class Trick(Base):
    __tablename__ = 'trick'

    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]
    video: Mapped[str] = mapped_column(nullable=True)
    level_id: Mapped[int] = mapped_column(ForeignKey('skate_level.id'))
    figure_id: Mapped[int] = mapped_column(ForeignKey('figure.id'))
    price: Mapped[float] = mapped_column(nullable=True)


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[intpk]
    user_id: Mapped[int]
    trick_id: Mapped[int]


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    video: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Numeric(10, 2))

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan"
    )
    course_orders: Mapped[list["CourseOrder"]] = relationship(
        "CourseOrder",
        back_populates="course",
    )


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    video: Mapped[str] = mapped_column(String)
    is_free: Mapped[bool] = mapped_column(Boolean)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id', ondelete='CASCADE'))

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="lessons"
    )


class CourseOrder(Base):
    __tablename__ = 'course_orders'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    payed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                               server_default=func.now())

    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="course_orders"
    )


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
