import uuid
from datetime import datetime

from aiogram import Bot
from dateutil.relativedelta import relativedelta
from yookassa import Payment

import app.keyboards.builder as bkb
from app.database.requests.subscription.delete import delete_subscription_by_tg_id
from app.database.requests.subscription.select import get_expired_subscriptions, get_subscription
from app.database.requests.subscription.update import update_subscription_end_date
from app.database.requests.tariff.select import get_tariff

from config import CHANNEL_ID, CHAT_ID


# async def send_message_middleware(bot: Bot, tg_id: int):
#     try:
#         await bot.ban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
#         await delete_subscription_by_tg_id(tg_id)
#         await bot.send_message(tg_id,
#                                f"<b>Ваша подписка закончилась!</b>\n\n",
#                                reply_markup=await bkb.user_panel(tg_id))
#         await bot.unban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
#
#     except Exception as e:
#         await bot.ban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
#         await delete_subscription_by_tg_id(tg_id)
#         await bot.unban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
#
#
# async def check_subscriptions(bot: Bot):
#     expired_users = await get_expired_subscriptions()
#     for subscription in expired_users:
#         tg_id = subscription.tg_id
#         await send_message_middleware(bot=bot, tg_id=tg_id)


async def send_message_middleware(bot: Bot, tg_id: int, message: str):
    try:
        # Забанить, удалить подписку, уведомить, разбанить
        await bot.ban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
        await bot.ban_chat_member(user_id=tg_id, chat_id=CHAT_ID)
        await delete_subscription_by_tg_id(tg_id)
        await bot.send_message(tg_id, message, reply_markup=await bkb.user_panel(tg_id))
        # await bot.unban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
    except Exception:
        # Если ошибка, всё равно удалить подписку и разбанить
        await bot.ban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)
        await bot.ban_chat_member(user_id=tg_id, chat_id=CHAT_ID)
        await delete_subscription_by_tg_id(tg_id)
        # await bot.unban_chat_member(user_id=tg_id, chat_id=CHANNEL_ID)


async def check_subscriptions(bot: Bot):
    expired_users = await get_expired_subscriptions()

    for subscription in expired_users:
        tg_id = subscription.tg_id
        tariff_id = subscription.tariff_id
        tariff = await get_tariff(tariff_id)

        # Получаем данные подписки (для автосписания)
        user_sub = await get_subscription(tg_id)
        if not user_sub or not user_sub.payment_method_id or not user_sub.is_active:
            await send_message_middleware(
                bot,
                tg_id,
                "<b>Срок вашей подписки истёк, и способ оплаты не найден.</b>\n"
                "Пожалуйста, оформите подписку заново для продолжения доступа."
            )
            continue

        try:
            payment = Payment.create({
                "amount": {
                    "value": f"{tariff.price}",
                    "currency": "RUB"
                },
                "payment_method_id": user_sub.payment_method_id,
                "capture": True,
                "metadata": {
                    "user_id": str(tg_id),
                    "subscription_id": str(user_sub.id)
                }
            }, str(uuid.uuid4()))

            if payment.status == "succeeded":
                new_end_date = datetime.now() + relativedelta(days=tariff.days_count)
                await update_subscription_end_date(tg_id, new_end_date, tariff_id)

                try:
                    await bot.send_message(
                        chat_id=tg_id,
                        text=f"<b>Ваша подписка была автоматически продлена до {new_end_date.strftime('%d.%m.%Y')} ✅</b>",
                        reply_markup=await bkb.user_panel(tg_id)
                    )
                except Exception as inner_e:
                    print(inner_e)
            else:
                await send_message_middleware(
                    bot,
                    tg_id,
                    "<b>Срок вашей подписки истёк, и нам не удалось автоматически продлить её.</b>\n"
                    "Пожалуйста, оформите подписку заново, чтобы продолжить доступ к закрытому каналу."
                )

        except Exception as e:
            print(f"Ошибка при автосписании у пользователя {tg_id}: {e}")
            await send_message_middleware(
                bot,
                tg_id,
                "<b>Произошла ошибка при попытке автосписания. Подписка удалена.</b>\n"
                "Пожалуйста, оформите её заново."
            )