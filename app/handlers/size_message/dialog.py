from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Column, Calendar, CalendarConfig, Row, PrevPage, \
    NextPage
from aiogram_dialog.widgets.text import Const, Format

from app.handlers.size_message.on_click import (on_back, on_back_menu,
                                                on_first_1, on_first_2,
                                                on_first_3, on_second_1,
                                                on_second_2, on_second_3,
                                                on_second_4, on_second_5,
                                                on_third_1, on_third_2,
                                                on_third_3, on_third_4,
                                                on_third_5)

from app.states import Size


size = Router()


size_dialog = Dialog(
    Window(
        Const(text="<b>Сколько тебе лет?</b>"),
    Column(
            Button(Const(text="<10"), id="on_first_1", on_click=on_first_1),
            Button(Const(text="10-14"), id="on_first_2", on_click=on_first_2),
            Button(Const(text=">15"), id="on_first_3", on_click=on_first_3),
            Button(Const(text="⏪ Назад"), id="on_back_menu", on_click=on_back_menu),
        ),
        state=Size.age
    ),
    Window(
        Const(text="<b>Какой у тебя рост?</b>"),
        Column(
            Button(Const(text="<160"), id="on_second_1", on_click=on_second_1),
            Button(Const(text="160-169"), id="on_second_2", on_click=on_second_2),
            Button(Const(text="170-179"), id="on_second_3", on_click=on_second_3),
            Button(Const(text="180-190"), id="on_second_4", on_click=on_second_4),
            Button(Const(text=">190"), id="on_second_5", on_click=on_second_5),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
            Button(Const(text="🏡 Главное меню"), id="on_back_menu", on_click=on_back_menu),
        ),
        state=Size.height
    ),
    Window(
        Const(text="<b>Какой у тебя размер ноги?</b>"),
        Column(
            Button(Const(text="<37"), id="on_third_1", on_click=on_third_1),
            Button(Const(text="37-39"), id="on_third_2", on_click=on_third_2),
            Button(Const(text="40-42"), id="on_third_3", on_click=on_third_3),
            Button(Const(text="43-45"), id="on_third_4", on_click=on_third_4),
            Button(Const(text=">45"), id="on_third_5", on_click=on_third_5),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
            Button(Const(text="🏡 Главное меню"), id="on_back_menu", on_click=on_back_menu),
        ),
        state=Size.foot_size
    )
)


@size.callback_query(F.data == "size_quiz")
async def size_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(Size.age, mode=StartMode.RESET_STACK)