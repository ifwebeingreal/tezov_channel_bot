import re

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from app.database.requests.trick.select import search_tricks_by_name

from app.states import UserSG


def check_text(text: str) -> str:
    if len(text) >= 500:
        raise ValueError("Слишком длинный ввод.")
    return text


async def correct_search_tricks(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
) -> None:
    # Получаем айди уровня и фигуры
    level_id = dialog_manager.dialog_data.get("skate_level_id")
    figure_id = dialog_manager.dialog_data.get("figure_id")

    # Преобразуем в int, если не None
    level_id = int(level_id) if level_id is not None else None
    figure_id = int(figure_id) if figure_id is not None else None

    print(f"🔍 Поиск трюков: '{text.lower()}', level_id={level_id}, figure_id={figure_id}")

    searched_tricks = await search_tricks_by_name(
        query=text,
        figure_id=figure_id,
        level_id=level_id
    )

    if searched_tricks:
        searched_tricks_data = [(trick.name, trick.id) for trick in searched_tricks]
        dialog_manager.dialog_data["searched_tricks_data"] = searched_tricks_data
        print(f"✅ Найдено трюков: {len(searched_tricks_data)}")
        await dialog_manager.switch_to(UserSG.searched_tricks)
    else:
        print("❌ Трюки не найдены")
        await message.answer("❌ <b>Темы не найдены!</b>")

