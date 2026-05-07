from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.course.select import get_course
from app.database.requests.course_order.select import get_course_order
from app.database.requests.lesson.select import get_lesson
from app.payments.course_pay import create_course_payment

user_course = Router()


@user_course.callback_query(F.data.startswith("usercourse_"))
async def user_check_course(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[1])
    course = await get_course(course_id)

    await callback.message.answer_video(
        video=course.video,
        caption=f"<b>{course.title}</b>\n\n"
                f"{course.description}",
        reply_markup=await bkb.user_course(course.id)
    )


@user_course.callback_query(F.data.startswith("user_check_free_"))
async def user_check_free_course(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    await callback.message.answer(
        "<b>Бесплатный контент:</b>",
        reply_markup=await bkb.free_lessons_for_user(course_id)
    )


@user_course.callback_query(F.data.startswith("freeuserlesson_"))
async def free_user_lesson(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[1])
    lesson = await get_lesson(lesson_id)

    await callback.message.answer_video(
        video=lesson.video,
        caption=f"<b>{lesson.title}</b>\n\n"
                f"{lesson.description}",
        reply_markup=await bkb.user_back_to_free(lesson.course_id)
    )


@user_course.callback_query(F.data.startswith("user_buy_course_"))
async def user_check_no_free_course(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await callback.message.delete()

    course_id = int(callback.data.split("_")[3])

    user = await get_course_order(callback.from_user.id, course_id)

    if not user:
        await create_course_payment(callback, bot, course_id)
    else:
        await callback.message.answer(
            "<b>Платный контент:</b>",
            reply_markup=await bkb.no_free_lessons_for_user(course_id)
        )


@user_course.callback_query(F.data.startswith("userlesson_"))
async def user_lesson(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    lesson_id = int(callback.data.split("_")[1])
    lesson = await get_lesson(lesson_id)

    await callback.message.answer_video(
        video=lesson.video,
        caption=f"<b>{lesson.title}</b>\n\n"
                f"{lesson.description}",
        reply_markup=await bkb.user_back_to_no_free(lesson.course_id)
    )