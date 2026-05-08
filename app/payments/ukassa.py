import asyncio
import uuid
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from dateutil.relativedelta import relativedelta
from yookassa import Payment, Configuration
from aiogram.types import CallbackQuery

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from config import CHANNEL_ID, CHAT_ID, ACCOUNT_ID, SECRET_KEY

from app.database.requests.tariff.select import get_tariff
from app.database.requests.subscription.select import get_subscription
from app.database.requests.subscription.add import set_subscription
from app.database.requests.admin.select import get_admins
from app.database.requests.subscription.update import update_subscription_end_date

Configuration.account_id = int(ACCOUNT_ID)
Configuration.secret_key = str(SECRET_KEY)


# def create_invoice(tariff, user_id):
#     return Payment.create({
#         "amount": {
#             "value": f"{tariff.price}",
#             "currency": "RUB"
#         },
#         "confirmation": {
#             "type": "redirect",
#             "return_url": "https://t.me/SkateChannel_bot"
#         },
#         "capture": True,
#         # "save_payment_method": True,
#         "description": f"{tariff.name} на {tariff.days_count} дней",
#         "metadata": {
#             "tariff_id": str(tariff.id),
#             "user_id": str(user_id)
#         }
#     }, uuid.uuid4())


def create_invoice(tariff, user_id):
    return Payment.create({
        "amount": {
            "value": f"{tariff.price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/SkateChannel_bot"
        },
        "capture": True,
        "save_payment_method": True,
        "description": f"{tariff.name} на {tariff.days_count} дней",
        "metadata": {
            "tariff_id": str(tariff.id),
            "user_id": str(user_id)
        }
    }, uuid.uuid4())


async def create_payment(callback: CallbackQuery, bot: Bot, tariff_id):
    user_id = callback.from_user.id
    tariff = await get_tariff(tariff_id)
    user = await get_subscription(user_id)
    payment = create_invoice(tariff, user_id)

    message = (
        f"<b>Вы выбрали тариф <u>{tariff.name}</u> на {tariff.days_count} дн.\n"
        f"Сумма к оплате: {tariff.price} ₽</b>\n\n"
        f"После оплаты способ оплаты будет сохранён, "
        f"и по окончании срока подписки произойдёт <b>автоматическое продление</b>.\n\n"
        f"Вы можете <b>отключить автосписание</b> в любое время в главном меню бота."
    ) if not user else None
    # (
#         f"""<b>Вы выбрали тариф {tariff.name} на {tariff.days_count} дн.
# Для оплаты на сумму {tariff.price} ₽ нажмите на кнопку "Оплатить"
# После оплаты подписка продлиться автоматически</b>"""
#     )
    await callback.message.edit_text(message, reply_markup=await bkb.ukassa_pay(payment.confirmation.confirmation_url))

    asyncio.create_task(check_payment_status(payment.id, callback, bot, tariff_id))


async def check_payment_status(payment_id: str, callback: CallbackQuery, bot: Bot, tariff_id):
    timeout = 600  # Таймаут 10 минут (600 секунд), чтобы не ждать вечно
    elapsed = 0
    while elapsed < timeout:
        payment = Payment.find_one(payment_id)
        if payment.status == "succeeded":
            method_id = payment.payment_method.id if payment.payment_method.saved else None
            await finalize_payment(callback, bot, tariff_id, method_id)
            break
        await asyncio.sleep(3)
        elapsed += 3
    else:
        # Если таймаут истек, можно отправить сообщение пользователю
        # await callback.message.answer("Время ожидания оплаты истекло. Попробуйте снова.")
        pass


async def finalize_payment(callback: CallbackQuery, bot: Bot, tariff_id, payment_method_id=None):
    user_id = callback.from_user.id
    user = await get_subscription(user_id)
    tariff = await get_tariff(tariff_id)

    if not user:
        now = datetime.now()
        await set_subscription(user_id, now, now + relativedelta(days=tariff.days_count), None, tariff_id)

        # Попытка разблокировать пользователя с обработкой ошибки
        try:
            await bot.unban_chat_member(user_id=user_id, chat_id=CHANNEL_ID)
            await bot.unban_chat_member(user_id=user_id, chat_id=CHAT_ID)
        except TelegramBadRequest as e:
            print(f"Ошибка при разблокировке пользователя {user_id}: {e}")
            # Можно добавить логику, например, отправить сообщение админу

        # Создание ссылки на канал
        try:
            link = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
            await callback.message.answer(
                f"<b>Спасибо за оплату! Добро пожаловать в закрытый канал!</b>\n"
                f"<b>Ссылка на канал: {link.invite_link}</b>",
                disable_web_page_preview=True,
                reply_markup=ikb.user_back_menu
            )
        except Exception as e:
            print(f"Ошибка при создании ссылки: {e}")
            await callback.message.answer(
                "<b>Спасибо за оплату! Возникла ошибка с доступом к каналу. Обратитесь в поддержку.</b>",
                reply_markup=ikb.user_back_menu
            )
    else:
        end = user.sub_end if isinstance(user.end_date, datetime) else datetime.fromisoformat(user.end_date)
        new_end = end + relativedelta(days=tariff.days_count)
        await update_subscription_end_date(user_id, new_end, tariff_id, None)
        await callback.message.answer(
            f"<b>Ваша подписка была продлена до {new_end.strftime('%d.%m.%Y')}</b>",
            reply_markup=ikb.user_back_menu
        )

    # Уведомление админов
    for admin in await get_admins():
        try:
            await bot.send_message(
                chat_id=admin.tg_id,
                text=f'<b>❗️Новая оплата❗️\n'
                     f'Пользователь <a href="tg://user?id={user_id}">{callback.from_user.full_name}</a>\n'
                     f'Название тарифа: {tariff.name}\n'
                     f'Стоимость: {tariff.price}₽\n'
                     f'Способ оплаты: ЮKassa</b>',
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin.tg_id}: {e}")






