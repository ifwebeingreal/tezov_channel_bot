import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.user.add import set_user
from app.database.requests.admin.select import get_admins
from app.database.requests.subscription.select import get_subscription
from app.database.requests.subscription.update import update_subscription_is_active


user = Router()


@user.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")

    await set_user(callback.from_user.id, callback.from_user.full_name, current_date)


@user.message(CommandStart())
async def start_command(message: Message):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    await set_user(message.from_user.id, message.from_user.full_name, current_date)

    await message.answer(f"""Привет, {message.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏

Что именно тебя интересует?
""",
                         reply_markup=await bkb.user_panel(message.from_user.id))

    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == message.from_user.id:
            await message.answer(f"Вы успешно авторизовались как администратор!",
                                 reply_markup=rkb.admin_menu)
            return


@user.callback_query(F.data == "channel")
async def channel(callback: CallbackQuery):
    await callback.answer("Мастерская временно недоступна!",
                          show_alert=True)
#     await callback.message.edit_text("""Мастерская - это закрытый канал, в котором ты будешь регулярно получать полезную информацию по всем аспектам скейтбординга🛹
#
# Расписание канала:
# ✅Пн - еженедельные разборы вопросов/ошибок
# ✅Ср - тренировка (новичок/начинающий)
# ✅Пт, вс - тренировка (средний/продвинутый)
#
# ✅Два раза в месяц тренировки, направленные на профилактику травм, офп, функциональный тренинг
# """,
#                                      reply_markup=await bkb.channel_panel(callback.from_user.id))


@user.callback_query(F.data == "my_subscription")
async def my_subscription(callback: CallbackQuery):
    subscription = await get_subscription(tg_id=callback.from_user.id)

    if not subscription:
        await callback.answer(
            text="У вас нет активной подписки",
            show_alert=True
        )

    else:
        await callback.message.edit_text(
            text=f"<b>Ваша подписка действует до {subscription.end_date[0:16]}</b>",
            reply_markup=ikb.user_back
        )


# @user.callback_query(F.data == "cancel_subscription")
# async def cancel_subscription(callback: CallbackQuery):
#     tg_id = callback.from_user.id
#     await update_subscription_is_active(tg_id, False)
#     await callback.answer(
#         text="Вы успешно отключили автосписание",
#         show_alert=True
#     )
#     await callback.message.edit_text(f"""Мастерская - это закрытый канал, в котором ты будешь регулярно получать полезную информацию по всем аспектам скейтбординга🛹
#
# Расписание канала:
# ✅Пн - еженедельные разборы вопросов/ошибок
# ✅Ср - тренировка (новичок/начинающий)
# ✅Пт, вс - тренировка (средний/продвинутый)
#
# ✅Два раза в месяц тренировки, направленные на профилактику травм, офп, функциональный тренинг
# """,
#                          reply_markup=await bkb.user_panel(callback.from_user.id))
#
#
# @user.callback_query(F.data == "activate_subscription")
# async def activate_subscription(callback: CallbackQuery):
#     tg_id = callback.from_user.id
#     await update_subscription_is_active(tg_id, True)
#     await callback.answer(
#         text="Вы успешно включили автосписание",
#         show_alert=True
#     )
#     await callback.message.edit_text(f"""Мастерская - это закрытый канал, в котором ты будешь регулярно получать полезную информацию по всем аспектам скейтбординга🛹
#
# Расписание канала:
# ✅Пн - еженедельные разборы вопросов/ошибок
# ✅Ср - тренировка (новичок/начинающий)
# ✅Пт, вс - тренировка (средний/продвинутый)
#
# ✅Два раза в месяц тренировки, направленные на профилактику травм, офп, функциональный тренинг
# """,
#                          reply_markup=await bkb.user_panel(callback.from_user.id))


@user.callback_query(F.data == "check_level")
async def check_level(callback: CallbackQuery):
    await callback.message.edit_text("""Пройди короткий тест и узнай, какой у тебя уровень владения скейтом✌️""",
                                     reply_markup=ikb.start_quiz)