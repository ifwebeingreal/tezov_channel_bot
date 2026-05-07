from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.user.add import set_user
from app.database.requests.admin.select import get_admins
from app.database.requests.user.select import get_statistics

back = Router()


@back.callback_query(F.data == "back")
async def admin_back(callback: CallbackQuery, state: FSMContext):
    daily_users, monthly_users, total_users = await get_statistics()
    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == callback.from_user.id:
            response = (
                f"<b>Добро пожаловать в админ-панель! 🎉</b>\n\n"
                f"📊 <b>Статистика пользователей:</b>\n"
                f"🌟 <b>За сегодня:</b> {daily_users} пользователей\n"
                f"📅 <b>За месяц:</b> {monthly_users} пользователей\n"
                f"🌍 <b>Всего:</b> {total_users} пользователей\n\n"
                f"✨<i>Спасибо за вашу работу!</i>"
            )

            await callback.message.edit_text(text=response,
                                 reply_markup=ikb.admin_panel)
            await state.clear()

            return


@back.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text=f"""Привет, {callback.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏
    
    Что именно тебя интересует?
    """,
                                     reply_markup=await bkb.user_panel(callback.from_user.id))
    except Exception:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer(text=f"""Привет, {callback.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏

Что именно тебя интересует?
""",
                                         reply_markup=await bkb.user_panel(callback.from_user.id))
    await state.clear()


@back.callback_query(F.data == "user_back_menu")
async def user_back_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"""Привет, {callback.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏

Что именно тебя интересует?
""",
                                 reply_markup=await bkb.user_panel(callback.from_user.id))
    await state.clear()