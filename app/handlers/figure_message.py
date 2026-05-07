from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.figure.add import set_figure
from app.database.requests.figure.select import get_figure
from app.database.requests.figure.delete import delete_figure
from app.database.requests.figure.update import update_figure_name

from app.states import AddFigure


figure = Router()


@figure.callback_query(F.data == "figures")
async def figures(callback: CallbackQuery):
    await callback.message.edit_text("<b>Выберите категорию катания для просмотр разделов:</b>",
                                     reply_markup=await bkb.figure_levels_cb())


@figure.callback_query(F.data.startswith("flevel_"))
async def figure_level(callback: CallbackQuery):
    level_id = int(callback.data.split("_")[1])
    await callback.message.edit_text("<b>Выберите раздел:</b>",
                                     reply_markup=await bkb.figure_cb(level_id))


@figure.callback_query(F.data.startswith("figure_"))
async def figure_info_panel(callback: CallbackQuery):
    figure_id = int(callback.data.split("_")[1])
    figure_info = await get_figure(figure_id)

    await callback.message.edit_text(f"<b>Информация о разделе:</b>\n\n"
                                     f"<b>Название:</b> {figure_info.name}\n\n"
                                     f"<b><i>Выберите действие:</i></b>",
                                     reply_markup=await bkb.edit_figure(figure_id))


@figure.callback_query(F.data.startswith("add_figure_"))
async def add_figure(callback: CallbackQuery, state: FSMContext):
    level_id = int(callback.data.split("_")[2])
    await callback.message.edit_text("<b>Введите название раздела:</b>",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddFigure.name)
    await state.update_data(level_id=level_id)


@figure.message(AddFigure.name)
async def add_figure(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 500:
        await state.update_data(name=message.text)
        data = await state.get_data()
        level_id = data.get("level_id")

        await set_figure(message.text, level_id)

        await message.answer("<b>Раздел успешно добавлен!</b>",
                             reply_markup=await bkb.figure_cb(level_id))

        await state.clear()

    else:
        await message.answer("<b>Введите корректное название раздела!</b>",
                             reply_markup=ikb.admin_cancel)


@figure.callback_query(F.data.startswith("editfig_"))
async def edit_figure(callback: CallbackQuery, state: FSMContext):
    figure_id = int(callback.data.split("_")[1])
    figure_info = await get_figure(figure_id)

    await callback.message.edit_text(f"<b>Введите новое название раздела:</b>\n\n"
                                     f"<b>Текущее название:</b> {figure_info.name}",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddFigure.new_name)
    await state.update_data(figure_id=figure_id)


@figure.message(AddFigure.new_name)
async def edit_figure(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 500:
        await state.update_data(name=message.text)
        data = await state.get_data()
        figure_id = data.get("figure_id")

        await update_figure_name(figure_id, message.text)
        figure = await get_figure(figure_id)

        await message.answer(f"<b>Информация о разделе:</b>\n\n"
                                         f"<b>Название:</b> {figure.name}\n\n"
                                         f"<b><i>Выберите действие:</i></b>",
                                         reply_markup=await bkb.edit_figure(figure_id))

        await state.clear()

    else:
        await message.answer("<b>Введите корректное название раздела!</b>",
                             reply_markup=ikb.admin_cancel)


@figure.callback_query(F.data.startswith("deletefig_"))
async def remove_figure(callback: CallbackQuery):
    figure_id = int(callback.data.split("_")[1])
    figure_info = await get_figure(figure_id)
    await delete_figure(figure_id)

    await callback.message.edit_text("<b>Раздел успешно удален!</b>",
                                     reply_markup=await bkb.figure_cb(figure_info.level_id))