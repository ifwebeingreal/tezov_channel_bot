# import asyncio
# import uuid
#
# from aiogram import Bot
# from yookassa import Payment
# from aiogram.types import CallbackQuery
#
# from config import TEST_ACCOUNT_ID, TEST_SECRET_KEY
#
# from app.database.requests.trick.select import get_trick_by_id
#
#
# async def create_payment(callback: CallbackQuery, bot: Bot, trick_id):
#     trick = await get_trick_by_id(trick_id)
#     payment = Payment.create({
#         "amount": {
#             "value": f"{trick.price}",
#             "currency": "RUB"
#         },
#         "confirmation": {
#             "type": "redirect",
#             "return_url": "https://t.me/Natali_clubBot"
#         },
#         "capture": True,
#         "description": f"{trick.name}",
#     }, uuid.uuid4())
#     user_id = callback.from_user.id
#     user = await get_subscription(user_id)
#     if not user:
#         await callback.message.edit_text(f"<b>Вы выбрали тариф {tariff.name} на {tariff.day_count} дн.\n"
#                                      f"Для оплаты на сумму {tariff.rub_price} ₽ нажмите на кнопку \"Оплатить\"</b>",
#                                       reply_markup=await bkb.ukassa_pay(payment.confirmation.confirmation_url))
#     else:
#         await callback.message.answer("❗️Для оплаты подписки на 1 месяц нажмите кнопку ОПЛАТИТЬ\n\n"
#                                       "После оплаты вы увидите ССЫЛКУ на вход в закрытый телеграм канал",
#                                       reply_markup=await bkb.ukassa_pay(payment.confirmation.confirmation_url))
#
#     asyncio.create_task(check_payment_status(payment.id, callback, bot, tariff_id))
#
#
# async def check_payment_status(payment_id: str, callback: CallbackQuery, bot: Bot, tariff_id):
#     while True:
#         payment = Payment.find_one(payment_id)  # Используем правильный идентификатор платежа
#         if payment.status == "succeeded":
#             await finalize_payment(callback, bot, tariff_id)
#             break
#
#         await asyncio.sleep(3)
#
#
# async def finalize_payment(callback: CallbackQuery, bot: Bot, tariff_id):
#     user_id = callback.from_user.id
#     user = await get_subscription(user_id)
#     tariff = await get_tariff(tariff_id)
#     last_date = tariff.day_count
#     text_10 = await get_text(10)
#
#     if not user:
#         current_date = datetime.now()
#         await set_subscription(tg_id=user_id,
#                            first_date=current_date,
#                            last_week=current_date + relativedelta(days=last_date) - relativedelta(days=7),
#                            is_week=False,
#                            last_three_days=current_date + relativedelta(days=last_date) - relativedelta(days=3),
#                            is_three_days=False,
#                            last_day=current_date + relativedelta(days=last_date) - relativedelta(days=1),
#                            is_last_day=False,
#                            sub_end=current_date + relativedelta(days=last_date))
#         link = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
#         await bot.send_message(chat_id=user_id,
#                                text=f"{text_10.text} {link.invite_link}")
#         for admin in ADMINS:
#             await bot.send_message(chat_id=admin,
#                                    text=f'<b>❗️Новая оплата❗️\n'
#                                         f'Пользователь <a href="tg://user?id={user_id}">{callback.from_user.full_name}</a>\n'
#                                         f'Название тарифа: {tariff.name}\n'
#                                         f'Cтоимость: {tariff.rub_price}\n'
#                                         f'Способ оплаты: ЮКАССА</b>',
#                                    parse_mode='HTML')
#     else:
#         await bot.send_message(
#             chat_id=user_id,
#             text="Ваша подписка была продлена на 1 месяц"
#         )
#
#
#
#
#
