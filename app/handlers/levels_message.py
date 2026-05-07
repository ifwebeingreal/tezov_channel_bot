from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.skate_level.add import set_skate_level
from app.database.requests.skate_level.select import get_skate_level
from app.database.requests.skate_level.delete import delete_skate_level
from app.database.requests.skate_level.update import update_skate_level

from app.states import AddLevel


level = Router()


@level.callback_query(F.data == 'levels')
async def levels(callback: CallbackQuery):
    await callback.message.edit_text("<b>Текущие уровни:</b>",
                                     reply_markup=await bkb.levels_cb())


@level.callback_query(F.data == 'add_level')
async def add_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Введите название уровня:</b>",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddLevel.name)


@level.message(AddLevel.name)
async def add_level(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await set_skate_level(message.text)

        await message.answer("<b>Уровень успешно добавлен!</b>",
                             reply_markup=await bkb.levels_cb())

        await state.clear()

    else:
        await message.answer("<b>Введите корректное название уровня!</b>",
                             reply_markup=ikb.admin_cancel)


@level.callback_query(F.data.startswith("level_"))
async def level_info(callback: CallbackQuery):
    level_id = int(callback.data.split("_")[1])
    level_info = await get_skate_level(level_id)

    await callback.message.edit_text(f"<b>Информация о уровне:</b>\n\n"
                                     f"<b>Название:</b> {level_info.name}\n\n"
                                     f"<b><i>Выберите действие:</i></b>",
                                     reply_markup=await bkb.edit_level(level_id))


@level.callback_query(F.data.startswith("deletelvl_"))
async def remove_level(callback: CallbackQuery):
    level_id = int(callback.data.split("_")[1])
    await delete_skate_level(level_id)

    await callback.message.edit_text("<b>Уровень успешно удален!</b>",
                                     reply_markup=await bkb.levels_cb())


@level.callback_query(F.data.startswith("editlvl_"))
async def edit_level(callback: CallbackQuery, state: FSMContext):
    level_id = int(callback.data.split("_")[1])
    level_info = await get_skate_level(level_id)

    await callback.message.edit_text(f"<b>Введите новое название уровня:</b>\n\n"
                                     f"<b>Текущее название:</b> {level_info.name}",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddLevel.new_name)
    await state.update_data(level_id=level_id)


@level.message(AddLevel.new_name)
async def edit_level(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(new_name=message.text)
        data = await state.get_data()
        level_id = data.get("level_id")

        await update_skate_level(level_id, message.text)

        level_info = await get_skate_level(level_id)

        await message.answer(f"<b>Информация о уровне:</b>\n\n"
                                         f"<b>Название:</b> {level_info.name}\n\n"
                                         f"<b><i>Выберите действие:</i></b>",
                                         reply_markup=await bkb.edit_level(level_id))

        await state.clear()

    else:
        await message.answer("<b>Введите корректное название уровня!</b>",
                             reply_markup=ikb.admin_cancel)