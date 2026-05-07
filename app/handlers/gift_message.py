from datetime import datetime

from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dateutil.relativedelta import relativedelta

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb
from app.database.requests.subscription.add import set_subscription
from app.database.requests.subscription.select import get_subscription
from app.database.requests.subscription.update import update_subscription_end_date
from app.database.requests.tariff.select import get_tariff

from app.states import Gift
from config import CHANNEL_ID, CHAT_ID

gift = Router()


@gift.callback_query(F.data == "gift")
async def tariffs_for_gift(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите тариф для подарка",
                                     reply_markup=await bkb.gift_tariffs_cb())
    await state.set_state(Gift.tariff_id)


@gift.callback_query(F.data.startswith("gifttariff_"), Gift.tariff_id)
async def tariff_selected(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(tariff_id=tariff_id)
    await callback.message.edit_text("Введите User ID пользователя:\n"
                                     "User ID можно найти тут: @username_to_id_bot",
                                     reply_markup=ikb.admin_cancel)
    await state.set_state(Gift.tg_id)


@gift.message(Gift.tg_id)
async def tg_id_selected(message: Message, state: FSMContext, bot: Bot):
    if message.text and message.text.isdigit():
        await state.update_data(tg_id=int(message.text))
        data = await state.get_data()
        subscription = await get_subscription(int(message.text))
        tariff_id = data.get("tariff_id")
        tg_id = data.get("tg_id")
        tariff = await get_tariff(tariff_id)
        if subscription:
            end = subscription.sub_end if isinstance(subscription.end_date, datetime) else datetime.fromisoformat(subscription.end_date)
            new_end = end + relativedelta(days=tariff.days_count)
            await update_subscription_end_date(tg_id, new_end, tariff_id, None)
            await message.answer(
                f"<b>У пользователя была подписка, поэтому она продлена до {new_end.strftime('%d.%m.%Y')}</b>",
                reply_markup=ikb.user_back_menu
            )
            await state.clear()
        else:
            now = datetime.now()
            await set_subscription(tg_id,
                                   now,
                                   now + relativedelta(days=tariff.days_count),
                                   None, tariff_id)

            try:
                await bot.unban_chat_member(tg_id, CHANNEL_ID)
                await bot.unban_chat_member(tg_id, CHAT_ID)
            except TelegramBadRequest as e:
                print(f"Ошибка при разблокировке пользователя {tg_id}: {e}")
                # Можно добавить логику, например, отправить сообщение админу

            # Создание ссылки на канал
            try:
                link = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
                await message.answer(
                    f"<b>Ссылка на канал: {link.invite_link}</b>",
                    disable_web_page_preview=True,
                )
                await message.answer("Ссылка была сгенерирована успешно!",
                                     reply_markup=ikb.admin_cancel)
                await state.clear()
            except:
                await message.answer("При создании ссылки на канал возникла ошибка.",
                                     reply_markup=ikb.admin_cancel)

    else:
        await message.answer("User ID должен быть числом!\n"
                             "User ID можно найти тут: @username_to_id_bot",
                             reply_markup=ikb.admin_cancel)
