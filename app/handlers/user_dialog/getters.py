import asyncio
import uuid

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from yookassa import Payment, Configuration

from app.database.requests.admin.select import get_admins
from app.database.requests.order.add import set_order
from app.database.requests.skate_level.select import get_skate_levels
from app.database.requests.figure.select import get_figures_by_level_id
from app.database.requests.trick.select import (get_tricks_by_level_id_and_figure_id,
                                                get_trick_by_id)
from app.database.requests.user.select import get_user

from app.states import UserSG
from config import SECRET_KEY, ACCOUNT_ID

Configuration.account_id = int(ACCOUNT_ID)
Configuration.secret_key = str(SECRET_KEY)


async def skate_levels_getter(dialog_manager: DialogManager, **kwargs):
    skate_levels = await get_skate_levels()

    return {
        "skate_levels": [(skate_level.name, skate_level.id) for skate_level in skate_levels]
    }


async def figures_getter(dialog_manager: DialogManager, **kwargs):
    level_id = dialog_manager.dialog_data.get("skate_level_id")
    print(level_id)
    figures = await get_figures_by_level_id(level_id)

    text = None

    if int(level_id) == 1:
        text = """Здесь собрана вся базовая информация об основах владения скейтом☝️
Пример: «Правильная постановка ног», Основы управления скейтом» и тд.
    """
    elif int(level_id) == 2:
        text = """Включает в себя всю самую необходимую информацию по базовым навыкам и элементам, из которых состоят более сложные трюки👌
Пример: «Паверслайд», «Олли», «Поп Шавит», «Основы трюков в рампе» и тд.
    """
    elif int(level_id) == 3:
        text="""В этой группе видео нет информации про базовые навыки и новые элементы. Тут только полноценные трюки средней и высокой сложности💪
Пример: «360 флип», «Блант ту фэйки», «Бс/Фс смит», «Липслайд по периле» и тд.
    """

    return {
        "figures": [(figure.name, figure.id) for figure in figures],
        "text": text
    }


async def tricks_getter(dialog_manager: DialogManager, **kwargs):
    level_id = dialog_manager.dialog_data.get("skate_level_id")
    figure_id = dialog_manager.dialog_data.get("figure_id")
    visual = dialog_manager.dialog_data.get("visual")
    tricks = await get_tricks_by_level_id_and_figure_id(level_id, figure_id)

    return {
        "tricks": [(trick.name, trick.id) for trick in tricks],
        "visual": visual
    }


async def prefix_tricks_getter(dialog_manager: DialogManager, **kwargs):
    searched_tricks_data = dialog_manager.dialog_data.get("searched_tricks_data")
    print(searched_tricks_data)

    return {
        "tricks_by_prefix": [(formatted[0], formatted[1]) for formatted in searched_tricks_data]
    }


async def trick_info_getter(dialog_manager: DialogManager, **kwargs):
    trick_id = dialog_manager.dialog_data.get("trick_id")
    trick = await get_trick_by_id(trick_id)

    if trick.video is None:
        return {
            "name": trick.name,
            "description": trick.description,
            # "price": trick.price if trick.price else "0.0"
        }

    file = MediaAttachment(type=ContentType.DOCUMENT, file_id=MediaId(file_id=trick.video))

    return {
        "name": trick.name,
        "description": trick.description,
        "video": file,
        # "price": trick.price if trick.price else "0.0"
    }


async def payment_getter(dialog_manager: DialogManager, bot: Bot, **kwargs):
    trick_id = dialog_manager.dialog_data.get("trick_id")
    trick = await get_trick_by_id(trick_id)
    user = await get_user(dialog_manager.event.from_user.id)

    payment = Payment.create({
        "amount": {
            "value": f'{trick.price}',
            "currency": 'RUB'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/skatebase_bot"
        },
        "capture": True,
        "description": f"{trick.name}",
    }, uuid.uuid4())

    dialog_manager.dialog_data.update(payment_id=payment.id, trick_id=trick_id)

    asyncio.create_task(check_trick_payment_status(payment.id,
                                                   user.tg_id,
                                                   trick_id,
                                                   bot,
                                                   user.first_name))

    return {
        "payment_url": payment.confirmation.confirmation_url,
        "payment_id": payment.id,
        "price": trick.price,
        "name": trick.name
    }


async def check_trick_payment_status(payment_id: str, user_id: int, trick_id: int, bot: Bot, first_name: str):
    while True:
        payment = Payment.find_one(payment_id)
        if payment.status == "succeeded":
            await finalize_trick_payment(user_id, trick_id, bot, first_name)
            break
        await asyncio.sleep(3)


async def finalize_trick_payment(user_id: int, trick_id: int, bot: Bot, first_name: str):
    trick = await get_trick_by_id(trick_id)
    admins = await get_admins()

    await set_order(user_id, trick_id)

    await bot.send_message(
        chat_id=user_id,
        text=f"✅ Оплата прошла успешно!\nВы получили доступ к теме: <b>{trick.name}</b>\n"
             f"Для просмотра темы нажмите кнопку \"Назад\" ☝️ и выберите тему еще раз.",
        parse_mode='HTML'
    )

    for admin in admins:
        await bot.send_message(
            chat_id=admin.tg_id,
            text=f'❗️Новая оплата❗️\n'
                 f'Пользователь <a href="tg://user?id={user_id}">{first_name}</a>\n'
                 f'Название темы: {trick.name}\n'
                 f'Стоимость: {trick.price}\n'
                 f'Способ оплаты: ЮКАССА',
            parse_mode='HTML'
        )




