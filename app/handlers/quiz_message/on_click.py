from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from app.handlers.quiz_message.total import total
from aiogram_dialog import StartMode
from app.states import UserSG  # Импортируем состояния базы знаний

import app.keyboards.inline as ikb

# Словарь для связи состояний с твоими ключами в dialog_data
STATE_KEYS = {
    "Quiz:how_much": "first",
    "Quiz:figures": "second",
    "Quiz:returns": "third",
    "Quiz:flat_expire": "fourth",
    "Quiz:ramp_expire": "fifth",
    "Quiz:rail": "sixth"
}


async def on_answer(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Достаем балл из ID (например "ans:5" -> 5)
    score = int(button.widget_id.split("_")[1])
    # Определяем ключ по текущему состоянию
    key = STATE_KEYS.get(manager.current_context().state.state)

    manager.dialog_data[key] = score
    await manager.next()


async def on_finish(callback: CallbackQuery, button: Button, manager: DialogManager):
    # Сохраняем последний ответ
    score = int(button.widget_id.split("_")[1])
    manager.dialog_data["sixth"] = score

    # Считаем сумму
    results = [manager.dialog_data.get(k, 0) for k in ["first", "second", "third", "fourth", "fifth", "sixth"]]
    total_score = sum(results)

    await manager.done()
    await total(callback, total_score)


async def on_back(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.back()


async def on_back_menu(callback: CallbackQuery, widget: Any, manager: DialogManager):
    # Запускаем диалог Базы знаний
    # mode=StartMode.RESET_STACK очистит историю (квиз закроется)
    # и откроет базу как новое главное меню
    await manager.start(UserSG.skate_level, mode=StartMode.RESET_STACK)
