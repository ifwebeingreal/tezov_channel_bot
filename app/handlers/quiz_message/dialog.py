import datetime
import re
from operator import itemgetter
from typing import Any

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Column, Calendar, CalendarConfig, Row, PrevPage, \
    NextPage
from aiogram_dialog.widgets.text import Const, Format

from app.handlers.quiz_message.on_click import (on_back_menu, on_back,
                                                on_first_1, on_first_2,
                                                on_first_3, on_first_4,
                                                on_second_1, on_second_2,
                                                on_second_3, on_second_4,
                                                on_second_5, on_third_1,
                                                on_third_2, on_third_5,
                                                on_third_3, on_third_4,
                                                on_fourth_1, on_fourth_5,
                                                on_fourth_2, on_fourth_3,
                                                on_fourth_4, on_fourth_6,
                                                on_fifth_1, on_fifth_6,
                                                on_fifth_2, on_fifth_3,
                                                on_fifth_4, on_fifth_5,
                                                on_sixth_1, on_sixth_3,
                                                on_sixth_5, on_sixth_2,
                                                on_sixth_4)

from app.states import Quiz


quiz = Router()


quiz_dialog = Dialog(
    Window(
        Const(text="<b>Как давно ты катаешься?</b>"),
    Column(
            Button(Const(text="Меньше 2 месяцев"), id="on_first_1", on_click=on_first_1),
            Button(Const(text="Около 6 месяцев"), id="on_first_2", on_click=on_first_2),
            Button(Const(text="1-2 года"), id="on_first_3", on_click=on_first_3),
            Button(Const(text="Более 2-ух лет"), id="on_first_4", on_click=on_first_4),
            Button(Const(text="⏪ Назад"), id="on_back_menu", on_click=on_back_menu),
        ),
        state=Quiz.how_much
    ),
    Window(
        Const(text="<b>На каких фигурах умеешь кататься?</b>"),
    Column(
            Button(Const(text="Ни на одной"), id="on_second_1", on_click=on_second_1),
            Button(Const(text="Только в рампе"), id="on_second_2", on_click=on_second_2),
            Button(Const(text="Только во флэту"), id="on_second_3", on_click=on_second_3),
            Button(Const(text="Во флэту и в рампе"), id="on_second_4", on_click=on_second_4),
            Button(Const(text="На всех что-то умею"), id="on_second_5", on_click=on_second_5),
            Button(Const(text="🏠 Главное меню"), id="on_back_menu", on_click=on_back_menu),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
        ),
        state=Quiz.figures
    ),
    Window(
        Const(text="<b>Как дела с разворотами на препятствии? (радиус / скат)</b>"),
    Column(
            Button(Const(text="Еще ничего не умею"), id="on_third_1", on_click=on_third_1),
            Button(Const(text="Осваиваю начальные развороты"), id="on_third_2", on_click=on_third_2),
            Button(Const(text="Умею несколько базовых разворотов"), id="on_third_3", on_click=on_third_3),
            Button(Const(text="Умею 5-15 разворотов"), id="on_third_4", on_click=on_third_4),
            Button(Const(text="С разворотами нет проблем"), id="on_third_5", on_click=on_third_5),
            Button(Const(text="🏠 Главное меню"), id="on_back_menu", on_click=on_back_menu),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
        ),
        state=Quiz.returns
    ),
    Window(
        Const(text="<b>Опиши свой уровень катания во флэту</b>"),
    Column(
            Button(Const(text="Ничего не умею / что такое флэт?"), id="on_fourth_1", on_click=on_fourth_1),
            Button(Const(text="Учу Олли и/или Шавит"), id="on_fourth_2", on_click=on_fourth_2),
            Button(Const(text="Умею Олли и парочку других трюков"), id="on_fourth_3", on_click=on_fourth_3),
            Button(Const(text="Умею несколько базовых трюков"), id="on_fourth_4", on_click=on_fourth_4),
            Button(Const(text="Базу умею, учу флипы"), id="on_fourth_5", on_click=on_fourth_5),
            Button(Const(text="Во всю практикую флипы"), id="on_fourth_6", on_click=on_fourth_6),
            Button(Const(text="🏠 Главное меню"), id="on_back_menu", on_click=on_back_menu),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
        ),
        state=Quiz.flat_expire
    ),
    Window(
        Const(text="<b>Как чувствуешь себя в рампе?</b>"),
    Column(
            Button(Const(text="Ничего не умею / что такое рампа?"), id="on_fifth_1", on_click=on_fifth_1),
            Button(Const(text="Умею только раскатку и развороты"), id="on_fifth_2", on_click=on_fifth_2),
            Button(Const(text="Умею один / несколько трюков"), id="on_fifth_3", on_click=on_fifth_3),
            Button(Const(text="Умею порядка 5-15 базовых трюков"), id="on_fifth_4", on_click=on_fifth_4),
            Button(Const(text="Умею 15-30 трюков"), id="on_fifth_5", on_click=on_fifth_5),
            Button(Const(text="Умею более 30 трюков"), id="on_fifth_6", on_click=on_fifth_6),
            Button(Const(text="🏠 Главное меню"), id="on_back_menu", on_click=on_back_menu),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
        ),
        state=Quiz.ramp_expire
    ),
    Window(
        Const(text="<b>По грани и/или периле скользишь?</b>"),
    Column(
            Button(Const(text="Нет / да что все эти слова значат?! "), id="on_sixth_1", on_click=on_sixth_1),
            Button(Const(text="Изучаю одно / несколько скольжений"), id="on_sixth_2", on_click=on_sixth_2),
            Button(Const(text="Умею 5-10 скольжений"), id="on_sixth_3", on_click=on_sixth_3),
            Button(Const(text="Умею 10-15 скольжений"), id="on_sixth_4", on_click=on_sixth_4),
            Button(Const(text="Умею больше 15-ти скольжений"), id="on_sixth_5", on_click=on_sixth_5),
            Button(Const(text="🏠 Главное меню"), id="on_back_menu", on_click=on_back_menu),
            Button(Const(text="⏪ Назад"), id="on_back", on_click=on_back),
        ),
        state=Quiz.rail
    )
)


@quiz.callback_query(F.data == "start_quiz")
async def quiz_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(Quiz.how_much, mode=StartMode.RESET_STACK)