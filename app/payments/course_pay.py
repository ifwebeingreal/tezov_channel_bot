import asyncio
import uuid

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from yookassa import Payment, Configuration
from aiogram.types import CallbackQuery

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.admin.select import get_admins
from app.database.requests.course.select import get_course
from app.database.requests.course_order.select import get_course_order
from app.database.requests.course_order.add import set_course_order

Configuration.account_id = 1106267
Configuration.secret_key = 'test_ERAYzpQ35G3AGugSlRliuhxQmroQ4yp7BG0tKvdS_nI'

# Configuration.account_id = 1124260
# Configuration.secret_key = "live_WJlzJLIkLd-jzsuEVNnemBasBrZNVg-sKqpwocRZMrE"



def create_course_invoice(course, tg_id):
    return Payment.create({
        "amount": {
            "value": f"{course.price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/SkateChannel_bot"
        },
        "capture": True,
        "save_payment_method": True,
        "description": f"{course.title}",
        "metadata": {
            "tariff_id": str(course.id),
            "user_id": str(tg_id)
        }
    }, uuid.uuid4())


async def create_course_payment(callback: CallbackQuery, bot: Bot, course_id):
    tg_id = callback.from_user.id
    course = await get_course(course_id)
    user = await get_course_order(tg_id, course_id)
    payment = create_course_invoice(course, tg_id)

    message = (
        f"<b>Вы выбрали тариф <u>{course.title}</u>\n"
        f"Сумма к оплате: {course.price} ₽</b>\n\n"
    ) if not user else None
    # (
#         f"""<b>Вы выбрали тариф {tariff.name} на {tariff.days_count} дн.
# Для оплаты на сумму {tariff.price} ₽ нажмите на кнопку "Оплатить"
# После оплаты подписка продлиться автоматически</b>"""
#     )
    await callback.message.answer(message, reply_markup=await bkb.ukassa_pay_course(payment.confirmation.confirmation_url))

    asyncio.create_task(check_course_payment_status(payment.id, callback, bot, course_id))


async def check_course_payment_status(payment_id: str, callback: CallbackQuery, bot: Bot, course_id):
    timeout = 600  # Таймаут 10 минут (600 секунд), чтобы не ждать вечно
    elapsed = 0
    while elapsed < timeout:
        payment = Payment.find_one(payment_id)
        if payment.status == "succeeded":
            await finalize_course_payment(callback, bot, course_id)
            break
        await asyncio.sleep(3)
        elapsed += 3
    else:
        # Если таймаут истек, можно отправить сообщение пользователю
        # await callback.message.answer("Время ожидания оплаты истекло. Попробуйте снова.")
        pass


async def finalize_course_payment(callback: CallbackQuery, bot: Bot, course_id):
    tg_id = callback.from_user.id
    user = await get_course_order(tg_id, course_id)
    course = await get_course(course_id)

    if not user:
        await set_course_order(tg_id, course_id)
        await callback.message.answer(
            "<b>Платный контент:</b>",
            reply_markup=await bkb.no_free_lessons_for_user(course_id)
        )
    else:
        pass

    # Уведомление админов
    for admin in await get_admins():
        try:
            await bot.send_message(
                chat_id=admin.tg_id,
                text=f'<b>❗️Новая оплата❗️\n'
                     f'Пользователь <a href="tg://user?id={tg_id}">{callback.from_user.full_name}</a>\n'
                     f'Название курса: {course.name}\n'
                     f'Стоимость: {course.price}₽\n'
                     f'Способ оплаты: ЮKassa</b>',
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin.tg_id}: {e}")






