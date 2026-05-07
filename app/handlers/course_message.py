from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.course.add import set_course
from app.database.requests.course.select import get_course
from app.database.requests.course.update import (update_course_price,
                                                 update_course_title,
                                                 update_course_video,
                                                 update_course_description)
from app.database.requests.course.delete import delete_course

from app.states import AddCourse, UpdateCourse


course = Router()


@course.callback_query(F.data == "courses")
async def all_courses(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "<b>Добавленные курсы:</b>",
            reply_markup=await bkb.courses_cb()
        )
    except Exception:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer(
            "<b>Добавленные курсы:</b>",
            reply_markup=await bkb.courses_cb()
        )


@course.callback_query(F.data == "add_course")
async def add_course(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите название курса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddCourse.title)


@course.message(AddCourse.title)
async def check_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(title=message.text)

        await message.answer(
            "<b>Введите стоимость описание</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddCourse.description)

    else:
        await message.answer(
            "<b>Заголовок должен быть текстом до 200 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.message(AddCourse.description)
async def check_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        await message.answer(
            "<b>Введите стоимость курса:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddCourse.price)

    else:
        await message.answer(
            "<b>Описание должно быть текстом до 1000 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.message(AddCourse.price)
async def check_price(message: Message, state: FSMContext):
    text = message.text.replace(',', '.').strip()  # заменяем запятую на точку

    try:
        price = float(text)

        if price < 0:
            await message.answer("❌ Цена не может быть отрицательной. "
                                 "Введите корректное значение.",
                                 reply_markup=ikb.admin_cancel)
            return

        await state.update_data(price=price)

        await message.answer(
            "<b>Отправьте видео-презентацию для курса:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddCourse.video)

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (например, 100 или 99.99).",
                             reply_markup=ikb.admin_cancel)


@course.message(AddCourse.video)
async def check_video(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)

        data = await state.get_data()

        title = data.get("title")
        description = data.get("description")
        video = data.get("video")
        price = data.get("price")

        await set_course(title=title,
                         description=description,
                         video=video,
                         price=price)

        await message.answer(
            "<b>Курс был успешно добавлен!</b>",
            reply_markup=await bkb.courses_cb()
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Пришлите видео!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.callback_query(F.data.startswith("course_"))
async def check_course_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[1])
    course_info = await get_course(course_id)

    await callback.message.answer_video(
        video=course_info.video,
        caption=f"<b>Панель управления курсом</b>\n\n"
                f"<b>Название:</b> <code>{course_info.title}</code>\n"
                f"<b>Описан:</b> {course_info.description}\n"
                f"<b>Стоимость:</b> {course_info.price} руб.\n\n"
                f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_course(course_id),
        disable_web_page_preview=True
    )


@course.callback_query(F.data.startswith("edit_course_title_"))
async def edit_course_title(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Введите новое название для курса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateCourse.new_title)
    await state.update_data(id=course_id)


@course.message(UpdateCourse.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(title=message.text)

        data = await state.get_data()

        id = data.get("id")
        title = data.get("title")

        await update_course_title(id, title)
        course_info = await get_course(id)

        await message.answer_video(
            video=course_info.video,
            caption=f"<b>Панель управления курсом</b>\n\n"
                    f"<b>Название:</b> <code>{course_info.title}</code>\n"
                    f"<b>Описан:</b> {course_info.description}\n"
                    f"<b>Стоимость:</b> {course_info.price} руб.\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_course(id),
            disable_web_page_preview=True
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Заголовок должен быть текстом до 200 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.callback_query(F.data.startswith("edit_course_desc_"))
async def edit_course_desc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Введите новое описание для курса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateCourse.new_description)
    await state.update_data(id=course_id)


@course.message(UpdateCourse.new_description)
async def check_new_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        data = await state.get_data()

        id = data.get("id")
        description = data.get("description")

        await update_course_description(id, description)
        course_info = await get_course(id)

        await message.answer_video(
            video=course_info.video,
            caption=f"<b>Панель управления курсом</b>\n\n"
                    f"<b>Название:</b> <code>{course_info.title}</code>\n"
                    f"<b>Описан:</b> {course_info.description}\n"
                    f"<b>Стоимость:</b> {course_info.price} руб.\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_course(id),
            disable_web_page_preview=True
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Описание должно быть текстом до 1000 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.callback_query(F.data.startswith("edit_course_price_"))
async def edit_course_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Введите новую стоимость для курса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateCourse.new_price)
    await state.update_data(id=course_id)


@course.message(UpdateCourse.new_price)
async def check_new_price(message: Message, state: FSMContext):
    text = message.text.replace(',', '.').strip()  # заменяем запятую на точку

    try:
        price = float(text)

        if price < 0:
            await message.answer("❌ Цена не может быть отрицательной. "
                                 "Введите корректное значение.",
                                 reply_markup=ikb.admin_cancel)
            return

        await state.update_data(price=price)

        data = await state.get_data()

        id = data.get("id")
        price = data.get("price")

        await update_course_price(id, price)
        course_info = await get_course(id)

        await message.answer_video(
            video=course_info.video,
            caption=f"<b>Панель управления курсом</b>\n\n"
                    f"<b>Название:</b> <code>{course_info.title}</code>\n"
                    f"<b>Описан:</b> {course_info.description}\n"
                    f"<b>Стоимость:</b> {course_info.price} руб.\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_course(id),
            disable_web_page_preview=True
        )

        await state.clear()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (например, 100 или 99.99).",
                             reply_markup=ikb.admin_cancel)


@course.callback_query(F.data.startswith("edit_course_video_"))
async def edit_course_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Отправьте новое видео для курса:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateCourse.new_video)
    await state.update_data(id=course_id)


@course.message(UpdateCourse.new_video)
async def check_new_video(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)

        data = await state.get_data()

        id = data.get("id")
        video = data.get("video")

        await update_course_video(id, video)
        course_info = await get_course(id)

        await message.answer_video(
            video=course_info.video,
            caption=f"<b>Панель управления курсом</b>\n\n"
                    f"<b>Название:</b> <code>{course_info.title}</code>\n"
                    f"<b>Описан:</b> {course_info.description}\n"
                    f"<b>Стоимость:</b> {course_info.price} руб.\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_course(id),
            disable_web_page_preview=True
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Отправьте видео!</b>",
            reply_markup=ikb.admin_cancel
        )


@course.callback_query(F.data.startswith("delete_course_"))
async def remove_course(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[2])
    await delete_course(course_id)

    await callback.message.answer(
        "<b>Курс был успешно удален!</b>",
        reply_markup=await bkb.courses_cb()
    )