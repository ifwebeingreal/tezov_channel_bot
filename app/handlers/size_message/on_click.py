from datetime import date, datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

import app.keyboards.inline as ikb
import app.keyboards.builder as bkb
from app.handlers.size_message.total import total_size

from app.states import Quiz

from app.handlers.quiz_message.total import total


async def on_back(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.back()


async def on_back_menu(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.done()

    await callback.message.edit_text(text=f"""Привет, {callback.from_user.first_name}! Добро пожаловать в Skate channel - место, где ты найдешь ответы на любые вопросы🙏

Что именно тебя интересует?
    """,
                                  reply_markup=await bkb.user_panel(callback.from_user.id))


async def on_first_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=1)
    await manager.next()


async def on_first_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=2)
    await manager.next()


async def on_first_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=3)
    await manager.next()


async def on_second_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=1)
    await manager.next()


async def on_second_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=2)
    await manager.next()


async def on_second_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=3)
    await manager.next()


async def on_second_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=4)
    await manager.next()


async def on_second_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=5)
    await manager.next()


async def on_third_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=1)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    result = int(first) + int(second) + int(third)
    await manager.done()
    await total_size(callback, result)


async def on_third_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=3)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    result = int(first) + int(second) + int(third)
    await manager.done()
    await total_size(callback, result)


async def on_third_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=5)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    result = int(first) + int(second) + int(third)
    await manager.done()
    await total_size(callback, result)


async def on_third_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=7)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    result = int(first) + int(second) + int(third)
    await manager.done()
    await total_size(callback, result)


async def on_third_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=9)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    result = int(first) + int(second) + int(third)
    await manager.done()
    await total_size(callback, result)

