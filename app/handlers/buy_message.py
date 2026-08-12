from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.subscription.select import get_subscription
from app.payments.ukassa import create_payment

buy = Router()


@buy.callback_query(F.data == "all_tariffs")
async def tariffs_menu(callback: CallbackQuery):
    # await callback.answer("Мастерская временно недоступна!",
    #                       show_alert=True)

    subscription = await get_subscription(tg_id=callback.from_user.id)

    if subscription:
        await callback.answer(
            text="Вы уже имеете активную подписку",
            show_alert=True
        )

        return

    await callback.message.edit_text("<b>Выберите тариф:</b>",
                                     reply_markup=await bkb.user_tariffs_cb())


@buy.callback_query(F.data.startswith("usertariff_"))
async def buy_tariff(callback: CallbackQuery, bot: Bot):
    # await callback.answer("Мастерская временно недоступна!",
    #                       show_alert=True)

    subscription = await get_subscription(tg_id=callback.from_user.id)

    if subscription:
        await callback.answer(
            text="Вы уже имеете активную подписку",
            show_alert=True
        )

        return
    tariff_id = int(callback.data.split("_")[1])
    await create_payment(callback, bot, tariff_id)


@buy.callback_query(F.data == "extend_subscription")
async def extend_subscription(callback: CallbackQuery, bot: Bot):
    # await callback.answer("Мастерская временно недоступна!",
    #                       show_alert=True)

    subscription = await get_subscription(tg_id=callback.from_user.id)

    if not subscription:
        await callback.answer(
            text="У вас нет активной подписки для продления",
            show_alert=True
        )

        return

    else:
        await callback.answer(
            text="Продление подписки временно недоступно!",
            show_alert=True
        )

        return

    await callback.message.edit_text("<b>Для продления подписки выберите тариф:</b>",
                                     reply_markup=await bkb.user_extend_cb())


@buy.callback_query(F.data.startswith("userextend_"))
async def extend_tariff(callback: CallbackQuery, bot: Bot):
    # await callback.answer("Мастерская временно недоступна!",
    #                       show_alert=True)
    #
    subscription = await get_subscription(tg_id=callback.from_user.id)

    if not subscription:
        await callback.answer(
            text="У вас нет активной подписки для продления",
            show_alert=True
        )

        return

    else:
        await callback.answer(
            text="Продление подписки временно недоступно!",
            show_alert=True
        )

        return

    tariff_id = int(callback.data.split("_")[1])
    await create_payment(callback, bot, tariff_id)
