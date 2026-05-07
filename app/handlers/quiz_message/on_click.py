from datetime import date, datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.states import Quiz

from app.handlers.quiz_message.total import total


async def on_back(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.back()


async def on_back_menu(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.done()

    await callback.message.edit_text("""Пройди короткий тест и узнай, какой у тебя уровень владения скейтом✌️""",
                                     reply_markup=ikb.start_quiz)


async def on_first_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=1)
    await manager.next()


async def on_first_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=2)
    await manager.next()


async def on_first_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=3)
    await manager.next()


async def on_first_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(first=4)
    await manager.next()


async def on_second_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=1)
    await manager.next()


async def on_second_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=2)
    await manager.next()


async def on_second_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=2)
    await manager.next()


async def on_second_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=4)
    await manager.next()


async def on_second_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(second=7)
    await manager.next()


async def on_third_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=1)
    await manager.next()


async def on_third_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=2)
    await manager.next()


async def on_third_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=2)
    await manager.next()


async def on_third_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=3)
    await manager.next()


async def on_third_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(third=4)
    await manager.next()


async def on_fourth_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=1)
    await manager.next()


async def on_fourth_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=2)
    await manager.next()


async def on_fourth_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=3)
    await manager.next()


async def on_fourth_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=5)
    await manager.next()


async def on_fourth_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=7)
    await manager.next()


async def on_fourth_6(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fourth=10)
    await manager.next()


async def on_fifth_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=1)
    await manager.next()


async def on_fifth_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=2)
    await manager.next()


async def on_fifth_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=3)
    await manager.next()


async def on_fifth_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=4)
    await manager.next()


async def on_fifth_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=7)
    await manager.next()


async def on_fifth_6(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(fifth=10)
    await manager.next()


async def on_sixth_1(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(sixth=1)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    fourth = manager.dialog_data.get("fourth")
    fifth = manager.dialog_data.get("fifth")
    sixth = manager.dialog_data.get("sixth")
    result = int(first) + int(second) + int(third) + int(fourth) + int(fifth) + int(sixth)
    await manager.done()
    await total(callback, result)


async def on_sixth_2(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(sixth=3)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    fourth = manager.dialog_data.get("fourth")
    fifth = manager.dialog_data.get("fifth")
    sixth = manager.dialog_data.get("sixth")
    result = int(first) + int(second) + int(third) + int(fourth) + int(fifth) + int(sixth)
    await manager.done()
    await total(callback, result)


async def on_sixth_3(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(sixth=5)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    fourth = manager.dialog_data.get("fourth")
    fifth = manager.dialog_data.get("fifth")
    sixth = manager.dialog_data.get("sixth")
    result = int(first) + int(second) + int(third) + int(fourth) + int(fifth) + int(sixth)
    await manager.done()
    await total(callback, result)


async def on_sixth_4(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(sixth=7)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    fourth = manager.dialog_data.get("fourth")
    fifth = manager.dialog_data.get("fifth")
    sixth = manager.dialog_data.get("sixth")
    result = int(first) + int(second) + int(third) + int(fourth) + int(fifth) + int(sixth)
    await manager.done()
    await total(callback, result)


async def on_sixth_5(callback: CallbackQuery, widget: Any, manager: DialogManager):
    manager.dialog_data.update(sixth=10)
    first = manager.dialog_data.get("first")
    second = manager.dialog_data.get("second")
    third = manager.dialog_data.get("third")
    fourth = manager.dialog_data.get("fourth")
    fifth = manager.dialog_data.get("fifth")
    sixth = manager.dialog_data.get("sixth")
    result = int(first) + int(second) + int(third) + int(fourth) + int(fifth) + int(sixth)
    print(result)
    await manager.done()
    await total(callback, result)