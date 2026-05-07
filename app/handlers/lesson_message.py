from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.lesson.add import set_lesson
from app.database.requests.lesson.select import get_lesson
from app.database.requests.lesson.update import (update_lesson_title,
                                                 update_lesson_description,
                                                 update_lesson_video,
                                                 update_lesson_is_free)
from app.database.requests.lesson.delete import delete_lesson
from app.database.requests.course.select import get_course

from app.states import AddLesson, UpdateLesson


lesson = Router()


@lesson.callback_query(F.data.startswith("lessons_"))
async def all_lessons(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[1])
    course = await get_course(course_id)

    await callback.message.answer(
        f"<b>Добавленные уроки для курса: <code>{course.title}</code></b>",
        reply_markup=await bkb.lessons_cb(course_id)
    )


@lesson.callback_query(F.data.startswith("add_lesson_"))
async def add_lesson(callback: CallbackQuery, state: FSMContext):
    course_id = int(callback.data.split("_")[2])

    await callback.message.edit_text(
        "<b>Введите название для урока:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddLesson.title)
    await state.update_data(course_id=course_id)


@lesson.message(AddLesson.title)
async def check_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(title=message.text)

        await message.answer(
            "<b>Пришлите описание для урока:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddLesson.description)

    else:
        await message.answer(
            "<b>Название должно быть до 200 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.message(AddLesson.description)
async def check_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        await message.answer(
            "<b>Пришлите видео для урока:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddLesson.video)

    else:
        await message.answer(
            "<b>Описание должно быть до 1000 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.message(AddLesson.video)
async def check_video(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)

        await message.answer(
            "<b>Сделать урок бесплатным?</b>",
            reply_markup=ikb.free_lesson_panel
        )

        await state.set_state(AddLesson.is_free)

    else:
        await message.answer(
            "<b>Пришлите видео!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.callback_query(F.data.startswith("free_"), AddLesson.is_free)
async def check_is_free(callback: CallbackQuery, state: FSMContext):
    free = callback.data.split("_")[1]

    if free == "yes":
        await state.update_data(is_free=True)
    elif free == "no":
        await state.update_data(is_free=False)

    data = await state.get_data()

    title = data.get("title")
    description = data.get("description")
    video = data.get("video")
    is_free = data.get("is_free")
    course_id = data.get("course_id")

    await set_lesson(title=title,
                     description=description,
                     video=video,
                     is_free=is_free,
                     course_id=course_id)

    await callback.message.edit_text(
        "<b>Урок был успешно добавлен!</b>",
        reply_markup=await bkb.lessons_cb(course_id)
    )

    await state.clear()


@lesson.callback_query(F.data.startswith("lesson_"))
async def check_lesson(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[1])
    lesson_info = await get_lesson(lesson_id)
    course = await get_course(lesson_info.course_id)

    await callback.message.answer_video(
        video=lesson_info.video,
        caption=f"<b>Панель управления уроком</b>\n\n"
                f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                f"<b>Описание:</b> {lesson_info.description}\n"
                f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_lesson(
            id=lesson_info.id,
            course_id=lesson_info.course_id,
            is_free=lesson_info.is_free,
        )
    )


@lesson.callback_query(F.data.startswith("edit_lesson_title_"))
async def edit_lesson_title(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Пришлите новое название для урока:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateLesson.new_title)
    await state.update_data(id=lesson_id)


@lesson.message(UpdateLesson.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 200:
        await state.update_data(title=message.text)

        data = await state.get_data()

        id = data.get("id")
        title = data.get("title")

        await update_lesson_title(id, title)
        lesson_info = await get_lesson(id)
        course = await get_course(lesson_info.course_id)

        await message.answer_video(
            video=lesson_info.video,
            caption=f"<b>Панель управления уроком</b>\n\n"
                    f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                    f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                    f"<b>Описание:</b> {lesson_info.description}\n"
                    f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_lesson(
                id=lesson_info.id,
                course_id=lesson_info.course_id,
                is_free=lesson_info.is_free,
            )
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Название должно быть до 200 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.callback_query(F.data.startswith("edit_lesson_desc_"))
async def edit_lesson_desc(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Введите новое описание для урока:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateLesson.new_description)
    await state.update_data(id=lesson_id)


@lesson.message(UpdateLesson.new_description)
async def check_new_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        data = await state.get_data()

        id = data.get("id")
        description = data.get("description")

        await update_lesson_description(id, description)
        lesson_info = await get_lesson(id)
        course = await get_course(lesson_info.course_id)

        await message.answer_video(
            video=lesson_info.video,
            caption=f"<b>Панель управления уроком</b>\n\n"
                    f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                    f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                    f"<b>Описание:</b> {lesson_info.description}\n"
                    f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_lesson(
                id=lesson_info.id,
                course_id=lesson_info.course_id,
                is_free=lesson_info.is_free,
            )
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Описание должно быть до 1000 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.callback_query(F.data.startswith("edit_lesson_video_"))
async def edit_lesson_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Отправьте новое видео для урока:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(UpdateLesson.new_video)
    await state.update_data(id=lesson_id)


@lesson.message(UpdateLesson.new_video)
async def check_new_video(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)

        data = await state.get_data()

        id = data.get("id")
        video = data.get("video")

        await update_lesson_video(id, video)
        lesson_info = await get_lesson(id)
        course = await get_course(lesson_info.course_id)

        await message.answer_video(
            video=lesson_info.video,
            caption=f"<b>Панель управления уроком</b>\n\n"
                    f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                    f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                    f"<b>Описание:</b> {lesson_info.description}\n"
                    f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                    f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_lesson(
                id=lesson_info.id,
                course_id=lesson_info.course_id,
                is_free=lesson_info.is_free,
            )
        )

        await state.clear()

    else:
        await message.answer(
            "<b>Описание должно быть до 1000 символов!</b>",
            reply_markup=ikb.admin_cancel
        )


@lesson.callback_query(F.data.startswith("edit_lesson_paid_"))
async def edit_lesson_paid(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[3])

    await update_lesson_is_free(lesson_id, False)
    lesson_info = await get_lesson(lesson_id)
    course = await get_course(lesson_info.course_id)

    await callback.message.answer_video(
        video=lesson_info.video,
        caption=f"<b>Панель управления уроком</b>\n\n"
                f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                f"<b>Описание:</b> {lesson_info.description}\n"
                f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_lesson(
            id=lesson_info.id,
            course_id=lesson_info.course_id,
            is_free=lesson_info.is_free,
        )
    )


@lesson.callback_query(F.data.startswith("edit_lesson_free_"))
async def edit_lesson_free(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[3])

    await update_lesson_is_free(lesson_id, True)
    lesson_info = await get_lesson(lesson_id)
    course = await get_course(lesson_info.course_id)

    await callback.message.answer_video(
        video=lesson_info.video,
        caption=f"<b>Панель управления уроком</b>\n\n"
                f"<b>Курс:</b> <code>{course.title}</code>\n\n"
                f"<b>Название:</b> <code>{lesson_info.title}</code>\n"
                f"<b>Описание:</b> {lesson_info.description}\n"
                f"<b>Бесплатный:</b> {'Да' if lesson_info.is_free else 'Нет'}\n\n"
                f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_lesson(
            id=lesson_info.id,
            course_id=lesson_info.course_id,
            is_free=lesson_info.is_free,
        )
    )


@lesson.callback_query(F.data.startswith("delete_lesson_"))
async def remove_lesson(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[2])
    lesson_info = await get_lesson(lesson_id)
    course_id = lesson_info.course_id
    await delete_lesson(lesson_id)

    await callback.message.answer(
        "<b>Урок был успешно удален!</b>",
        reply_markup=await bkb.lessons_cb(course_id)
    )
