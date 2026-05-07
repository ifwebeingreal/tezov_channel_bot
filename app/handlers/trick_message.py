from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.trick.add import set_trick
from app.database.requests.trick.select import get_trick_by_id
from app.database.requests.trick.delete import delete_trick
from app.database.requests.trick.update import (update_trick_name, update_trick_video,
    update_trick_description, update_trick_price)

from app.states import AddTrick, CheckTrick


trick = Router()


@trick.callback_query(F.data == "tricks")
async def tricks(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("<b>Для поиска темы выберите уровень катания:</b>",
                                         reply_markup=await bkb.trick_levels_cb())
    except:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer("<b>Для поиска темы выберите уровень катания:</b>",
                                      reply_markup=await bkb.trick_levels_cb())

    await state.set_state(CheckTrick.level_id)


@trick.callback_query(F.data.startswith("tlevel_"), CheckTrick.level_id)
async def trick_level(callback: CallbackQuery, state: FSMContext):
    level_id = int(callback.data.split("_")[1])
    await callback.message.edit_text("<b>Выберите раздел:</b>",
                                     reply_markup=await bkb.trick_figure_cb(level_id))

    await state.update_data(level_id=level_id)
    await state.set_state(CheckTrick.figure_id)


@trick.callback_query(F.data.startswith("tfigure_"), CheckTrick.figure_id)
async def trick_figure(callback: CallbackQuery, state: FSMContext):
    figure_id = int(callback.data.split("_")[1])
    await state.update_data(figure_id=figure_id)
    data = await state.get_data()
    level_id = data.get("level_id")
    figure_id = data.get("figure_id")

    await callback.message.edit_text("<b>Добавленные темы:</b>",
                                     reply_markup=await bkb.trick_cb(level_id, figure_id))

    await state.clear()


@trick.callback_query(F.data.startswith("add_trick_"))
async def add_trick(callback: CallbackQuery, state: FSMContext):
    level_id = int(callback.data.split("_")[2])
    figure_id = int(callback.data.split("_")[3])

    await state.update_data(level_id=level_id,
                            figure_id=figure_id)

    await callback.message.edit_text("<b>Введите название темы:</b>",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddTrick.name)


@trick.message(AddTrick.name)
async def add_trick(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 500:
        await state.update_data(name=message.text)

        await message.answer("<b>Введите описание для темы:</b>",
                             reply_markup=ikb.admin_cancel)

        await state.set_state(AddTrick.description)

    else:
        await message.answer("<b>Введите корректное название темы!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.message(AddTrick.description)
async def add_trick(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1300:
        await state.update_data(description=message.text)

        await message.answer("<b>Пришлите видео для темы:</b>",
                             reply_markup=ikb.skip_video)

        await state.set_state(AddTrick.video)

    else:
        await message.answer("<b>Описание должно быть не более 1300 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.callback_query(F.data == "video_skip", AddTrick.video)
async def video_skip_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(video=None)

    await callback.message.edit_text("<b>Введите стоимость темы</b>",
                         reply_markup=ikb.trick_cancel)

    await state.set_state(AddTrick.price)


@trick.message(AddTrick.video)
async def add_trick(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)

        await message.answer("<b>Введите стоимость темы</b>",
                             reply_markup=ikb.trick_cancel)

        await state.set_state(AddTrick.price)

    else:
        await message.answer("<b>Пришлите видео для темы!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.callback_query(F.data == "free", AddTrick.price)
async def free_trick(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    level_id = data.get("level_id")
    figure_id = data.get("figure_id")
    name = data.get("name")
    description = data.get("description")
    video = data.get("video")

    await set_trick(name=name,
                    description=description,
                    video=video,
                    figure_id=figure_id,
                    level_id=level_id,
                    price=None)

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Тема была успешно добавлена!</b>",
                                  reply_markup=await bkb.trick_cb(level_id, figure_id))



@trick.callback_query(F.data.startswith("trick_"))
async def trick_info_panel(callback: CallbackQuery):
    trick_id = int(callback.data.split("_")[1])
    trick_info = await get_trick_by_id(trick_id)

    await callback.answer()
    await callback.message.delete()

    if trick_info.video:
        await callback.message.answer_video(video=trick_info.video,
                                            caption=f"<b>Название темы:</b> {trick_info.name}\n"
                                                    f"<b>Описание темы:</b> {trick_info.description}\n"
                                                    f"<b>Стоимость темы:</b> {trick_info.price or '0.0'} руб.\n\n"
                                                    f"<b><i>Выберите действие:</i></b>",
                                            reply_markup=await bkb.edit_trick(trick_id))
    else:
        await callback.message.answer(text=f"<b>Название темы:</b> {trick_info.name}\n"
                                                    f"<b>Описание темы:</b> {trick_info.description}\n"
                                                    f"<b>Стоимость темы:</b> {trick_info.price or '0.0'} руб.\n\n"
                                                    f"<b><i>Выберите действие:</i></b>",
                                            reply_markup=await bkb.edit_trick(trick_id))


@trick.message(AddTrick.price)
async def add_trick_price(message: Message, state: FSMContext):
    text = message.text.replace(',', '.').strip()  # заменяем запятую на точку

    try:
        price = float(text)

        if price < 0:
            await message.answer("❌ Цена не может быть отрицательной. Введите корректное значение.")
            return

        await state.update_data(price=price)
        data = await state.get_data()
        level_id = data.get("level_id")
        figure_id = data.get("figure_id")
        name = data.get("name")
        description = data.get("description")
        video = data.get("video")

        await set_trick(name=name,
                        description=description,
                        video=video,
                        figure_id=figure_id,
                        level_id=level_id,
                        price=price)

        await message.answer("<b>Тема была успешно добавлена!</b>",
                             reply_markup=await bkb.trick_cb(level_id, figure_id))

        await state.clear()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (например, 100 или 99.99).")



@trick.callback_query(F.data.startswith("edittrick_"))
async def edit_trick(callback: CallbackQuery, state: FSMContext):
    trick_id = int(callback.data.split("_")[1])

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(f"<b>Введите новое название темы:</b>\n\n",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddTrick.new_name)
    await state.update_data(trick_id=trick_id)


@trick.message(AddTrick.new_name)
async def edit_trick(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 500:
        await state.update_data(name=message.text)
        data = await state.get_data()
        trick_id = data.get("trick_id")

        await update_trick_name(trick_id, message.text)
        trick = await get_trick_by_id(trick_id)

        if trick.video:
            await message.answer_video(video=trick.video,
                                       caption=f"<b>Название темы:</b> {trick.name}\n"
                                               f"<b>Описание темы:</b> {trick.description}\n\n"
                                               f"<b><i>Выберите действие:</i></b>",
            reply_markup=await bkb.edit_trick(trick_id))
        else:
            await message.answer(text=f"<b>Название темы:</b> {trick.name}\n"
                                               f"<b>Описание темы:</b> {trick.description}\n\n"
                                               f"<b><i>Выберите действие:</i></b>",
                                       reply_markup=await bkb.edit_trick(trick_id))

        await state.clear()

    else:
        await message.answer("<b>Введите корректное название темы!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.callback_query(F.data.startswith("edittrickdesc_"))
async def edit_trick(callback: CallbackQuery, state: FSMContext):
    trick_id = int(callback.data.split("_")[1])

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(f"<b>Введите новое описание темы:</b>\n\n",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddTrick.new_description)
    await state.update_data(trick_id=trick_id)


@trick.message(AddTrick.new_description)
async def edit_trick(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1300:
        await state.update_data(description=message.text)
        data = await state.get_data()
        trick_id = data.get("trick_id")

        await update_trick_description(trick_id, message.text)
        trick = await get_trick_by_id(trick_id)

        if trick.video:
            await message.answer_video(video=trick.video,
                                       caption=f"<b>Название темы:</b> {trick.name}\n"
                                               f"<b>Описание темы:</b> {trick.description}\n\n"
                                               f"<b><i>Выберите действие:</i></b>",
                                       reply_markup=await bkb.edit_trick(trick_id))
        else:
            await message.answer(text=f"<b>Название темы:</b> {trick.name}\n"
                                      f"<b>Описание темы:</b> {trick.description}\n\n"
                                      f"<b><i>Выберите действие:</i></b>",
                                 reply_markup=await bkb.edit_trick(trick_id))

        await state.clear()

    else:
        await message.answer("<b>Описание темы должно быть не более 1300 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.callback_query(F.data.startswith("edittrickvideo_"))
async def edit_trick(callback: CallbackQuery, state: FSMContext):
    trick_id = int(callback.data.split("_")[1])

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(f"<b>Пришлите новое видео темы:</b>\n\n",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddTrick.new_video)
    await state.update_data(trick_id=trick_id)


@trick.message(AddTrick.new_video)
async def edit_trick(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)
        data = await state.get_data()
        trick_id = data.get("trick_id")

        await update_trick_video(trick_id, message.video.file_id)
        trick = await get_trick_by_id(trick_id)

        if trick.video:
            await message.answer_video(video=trick.video,
                                       caption=f"<b>Название темы:</b> {trick.name}\n"
                                               f"<b>Описание темы:</b> {trick.description}\n\n"
                                               f"<b><i>Выберите действие:</i></b>",
                                       reply_markup=await bkb.edit_trick(trick_id))
        else:
            await message.answer(text=f"<b>Название темы:</b> {trick.name}\n"
                                      f"<b>Описание темы:</b> {trick.description}\n\n"
                                      f"<b><i>Выберите действие:</i></b>",
                                 reply_markup=await bkb.edit_trick(trick_id))

        await state.clear()

    else:
        await message.answer("<b>Пришлите корректное видео трюка!</b>",
                             reply_markup=ikb.admin_cancel)


@trick.callback_query(F.data.startswith("edittrickprice_"))
async def edit_trick_price(callback: CallbackQuery, state: FSMContext):
    trick_id = int(callback.data.split("_")[1])

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer(f"<b>Введите новую стоимость темы:</b>\n\n",
                                     reply_markup=ikb.admin_cancel)

    await state.set_state(AddTrick.new_price)
    await state.update_data(trick_id=trick_id)


@trick.message(AddTrick.new_price)
async def wait_price(message: Message, state: FSMContext):
    text = message.text.replace(',', '.').strip()  # заменяем запятую на точку

    try:
        price = float(text)

        if price < 0:
            await message.answer("❌ Цена не может быть отрицательной. Введите корректное значение.")
            return

        await state.update_data(price=price)
        data = await state.get_data()
        trick_id = data.get("trick_id")

        await update_trick_price(trick_id, price)
        trick = await get_trick_by_id(trick_id)

        if trick.video:
            await message.answer_video(video=trick.video,
                                       caption=f"<b>Название темы:</b> {trick.name}\n"
                                               f"<b>Описание темы:</b> {trick.description}\n\n"
                                               f"<b><i>Выберите действие:</i></b>",
                                       reply_markup=await bkb.edit_trick(trick_id))
        else:
            await message.answer(text=f"<b>Название темы:</b> {trick.name}\n"
                                      f"<b>Описание темы:</b> {trick.description}\n\n"
                                      f"<b><i>Выберите действие:</i></b>",
                                 reply_markup=await bkb.edit_trick(trick_id))

        await state.clear()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (например, 100 или 99.99).")


@trick.callback_query(F.data.startswith("edittrickfree_"))
async def edit_trick_free(callback: CallbackQuery):
    trick_id = int(callback.data.split("_")[1])
    await update_trick_price(trick_id, None)
    trick = await get_trick_by_id(trick_id)
    await callback.answer()
    await callback.message.delete()
    if trick.video:
        await callback.message.answer_video(video=trick.video,
                                   caption=f"<b>Название темы:</b> {trick.name}\n"
                                           f"<b>Описание темы:</b> {trick.description}\n\n"
                                           f"<b><i>Выберите действие:</i></b>",
                                   reply_markup=await bkb.edit_trick(trick_id))
    else:
        await callback.message.answer(text=f"<b>Название темы:</b> {trick.name}\n"
                                  f"<b>Описание темы:</b> {trick.description}\n\n"
                                  f"<b><i>Выберите действие:</i></b>",
                             reply_markup=await bkb.edit_trick(trick_id))


@trick.callback_query(F.data.startswith("deletevideo_"))
async def delete_video_for_trick(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    trick_id = int(callback.data.split("_")[1])

    await update_trick_video(trick_id, None)

    trick_info = await get_trick_by_id(trick_id)

    await callback.message.answer(text=f"<b>Название темы:</b> {trick_info.name}\n"
                                       f"<b>Описание темы:</b> {trick_info.description}\n\n"
                                       f"<b><i>Выберите действие:</i></b>",
                                  reply_markup=await bkb.edit_trick(trick_id))


@trick.callback_query(F.data.startswith("deletetrick_"))
async def remove_trick(callback: CallbackQuery):
    trick_id = int(callback.data.split("_")[1])
    trick = await get_trick_by_id(trick_id)
    await callback.answer()
    await callback.message.delete()
    await delete_trick(trick_id)
    await callback.message.answer("<b>Тема была успешно удалена!</b>",
                                  reply_markup=await bkb.trick_cb(trick.level_id, trick.figure_id))


