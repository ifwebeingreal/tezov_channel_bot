import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.filters.admin_filter import AdminProtect
from app.filters.check_sub import CheckSubscription, CheckSubscriptionCallback
from config import BOT_TOKEN

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.back_message import back
from app.handlers.tariff_message import tariff
from app.handlers.buy_message import buy
from app.handlers.gift_message import gift
from app.handlers.trick_message import trick
from app.handlers.figure_message import figure
from app.handlers.levels_message import level
from app.handlers.course_message import course
from app.handlers.lesson_message import lesson
from app.handlers.user_course_message import user_course

from app.handlers.quiz_message.dialog import quiz, quiz_dialog
from app.handlers.user_dialog.dialog import user_dialog, user as user_base
from app.handlers.size_message.dialog import size, size_dialog

from app.database.models import create_db

from app.apsched.check_sub import check_subscriptions


scheduler = AsyncIOScheduler()


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # dp.message.middleware(CheckSubscription())
    # dp.callback_query.middleware(CheckSubscriptionCallback())

    admin.message.middleware(AdminProtect())
    admin.callback_query.middleware(AdminProtect())
    course.message.middleware(AdminProtect())
    course.callback_query.middleware(AdminProtect())
    lesson.message.middleware(AdminProtect())
    lesson.callback_query.middleware(AdminProtect())
    user_course.message.middleware(AdminProtect())
    user_course.callback_query.middleware(AdminProtect())

    dp.include_router(user)
    dp.include_router(buy)
    dp.include_router(admin)
    dp.include_router(gift)
    dp.include_router(tariff)
    dp.include_router(back)
    dp.include_router(level)
    dp.include_router(figure)
    dp.include_router(trick)
    dp.include_router(course)
    dp.include_router(lesson)
    dp.include_router(user_course)

    dp.include_router(quiz_dialog)
    dp.include_router(quiz)

    dp.include_router(user_base)
    dp.include_router(user_dialog)

    dp.include_router(size)
    dp.include_router(size_dialog)

    setup_dialogs(dp)

    # scheduler.add_job(check_subscriptions, 'interval', seconds=5, kwargs={'bot': bot})
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
