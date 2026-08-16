import datetime
from pyexpat.errors import messages
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from app.database.requests.figure.select import get_figures_by_level_id
from app.database.requests.order.select import get_order
from app.database.requests.skate_level.select import get_skate_level
from app.database.requests.trick.select import get_tricks_by_level_id_and_figure_id, get_trick_by_id
from app.database.requests.subscription.select import get_subscription

import app.keyboards.builder as bkb

from app.states import UserSG, Quiz


async def on_start_quiz_from_base(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Запускаем диалог квиза поверх текущего
    await manager.start(Quiz.how_much, mode=StartMode.NORMAL)


async def on_back(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.back()


async def on_back_2(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.switch_to(UserSG.tricks)


async def on_back_menu(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()

    await callback.message.edit_text(text=f"""Привет, {callback.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏

Что именно тебя интересует?
""",
                                     reply_markup=await bkb.user_panel(callback.from_user.id))

async def on_skate_level(callback: CallbackQuery, widget: Any,
                         dialog_manager: DialogManager, skate_level_id: int):
    figures = await get_figures_by_level_id(skate_level_id)

    if not figures:
        await callback.answer("Тут пока ничего нет, но скоро появится😉", show_alert=True)
        return  # 🔴 Обязательно!

    dialog_manager.dialog_data.update(skate_level_id=skate_level_id)

    await dialog_manager.next()


async def on_figure(callback: CallbackQuery, widget: Any,
                    dialog_manager: DialogManager, figure_id: int):
    level_id = int(dialog_manager.dialog_data.get("skate_level_id"))
    tricks = await get_tricks_by_level_id_and_figure_id(level_id, figure_id)

    if not tricks:
        await callback.answer("Тут пока ничего нет, но скоро появится😉", show_alert=True)
        return

    dialog_manager.dialog_data.update(figure_id=figure_id)
    await dialog_manager.next()


async def on_one_list(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(visual=False)
    await dialog_manager.next()


async def on_nine_in_one(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(visual=True)
    await dialog_manager.next()


async def on_trick(callback: CallbackQuery, widget: Any,
                   dialog_manager: DialogManager, trick_id: int):
    trick = await get_trick_by_id(int(trick_id))
    order = await get_order(callback.from_user.id, trick_id)
    subscription = await get_subscription(callback.from_user.id)

    if not trick:
        await callback.answer("Тут пока ничего нет, но скоро появится😉", show_alert=True)
        return

    if order or subscription:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.next()
        return

    if trick.price:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.switch_to(UserSG.pay_menu)
        return

    dialog_manager.dialog_data.update(trick_id=trick_id)
    await dialog_manager.next()


async def on_trick_2(callback: CallbackQuery, widget: Any,
                   dialog_manager: DialogManager, trick_id: int):
    trick = await get_trick_by_id(int(trick_id))
    order = await get_order(callback.from_user.id, int(trick_id))
    subscription = await get_subscription(callback.from_user.id)

    if not trick:
        await callback.answer("Тут пока ничего нет, но скоро появится😉", show_alert=True)
        return

    if order or subscription:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.next()
        return

    if trick.price:
        dialog_manager.dialog_data.update(trick_id=trick_id)
        await dialog_manager.switch_to(UserSG.pay_menu)
        return

    dialog_manager.dialog_data.update(trick_id=trick_id)
    await dialog_manager.switch_to(UserSG.trick_info)

async def on_trick_info(callback: CallbackQuery, widget: Any,
                         dialog_manager: DialogManager):
    await dialog_manager.next()


