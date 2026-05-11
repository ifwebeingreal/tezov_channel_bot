from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const

from app.states import Quiz
# Не забудь в файле on_click.py тоже поменять .split(":") на .split("_")
from app.handlers.quiz_message.on_click import (
    on_back_menu, on_back, on_answer, on_finish
)

quiz = Router()

quiz_dialog = Dialog(
    Window(
        Const(text="<b>Как давно ты катаешься?</b>"),
        Column(
            Button(Const("Меньше 2 месяцев"), id="ans_1", on_click=on_answer),
            Button(Const("Около 6 месяцев"), id="ans_2", on_click=on_answer),
            Button(Const("1-2 года"), id="ans_3", on_click=on_answer),
            Button(Const("Более 2-ух лет"), id="ans_4", on_click=on_answer),
            Button(Const("⏪ Назад"), id="back_menu_btn", on_click=on_back_menu),
        ),
        state=Quiz.how_much
    ),
    Window(
        Const(text="<b>На каких фигурах умеешь кататься?</b>"),
        Column(
            Button(Const("Ни на одной"), id="ans_1", on_click=on_answer),
            Button(Const("Только в рампе"), id="ans_2", on_click=on_answer),
            Button(Const("Только во флэту"), id="ans_3", on_click=on_answer),
            Button(Const("Во флэту и в рампе"), id="ans_4", on_click=on_answer),
            Button(Const("На всех что-то умею"), id="ans_7", on_click=on_answer),
            Button(Const("🏠 Главное меню"), id="back_menu_btn_2", on_click=on_back_menu),
            Button(Const("⏪ Назад"), id="back_btn_2", on_click=on_back),
        ),
        state=Quiz.figures
    ),
    Window(
        Const(text="<b>Как дела с разворотами на препятствии? (радиус / скат)</b>"),
        Column(
            Button(Const("Еще ничего не умею"), id="ans_1", on_click=on_answer),
            Button(Const("Осваиваю начальные развороты"), id="ans_2", on_click=on_answer),
            Button(Const("Умею несколько базовых"), id="ans_3", on_click=on_answer),
            Button(Const("Умею 5-15 разворотов"), id="ans_4", on_click=on_answer),
            Button(Const("С разворотами нет проблем"), id="ans_5", on_click=on_answer),
            Button(Const("🏠 Главное меню"), id="back_menu_btn_3", on_click=on_back_menu),
            Button(Const("⏪ Назад"), id="back_btn_3", on_click=on_back),
        ),
        state=Quiz.returns
    ),
    Window(
        Const(text="<b>Опиши свой уровень катания во флэту</b>"),
        Column(
            Button(Const("Ничего не умею"), id="ans_1", on_click=on_answer),
            Button(Const("Учу Олли и/или Шавит"), id="ans_2", on_click=on_answer),
            Button(Const("Умею Олли + трюки"), id="ans_3", on_click=on_answer),
            Button(Const("Несколько базовых"), id="ans_5", on_click=on_answer),
            Button(Const("Базу умею, учу флипы"), id="ans_7", on_click=on_answer),
            Button(Const("Практикую флипы"), id="ans_10", on_click=on_answer),
            Button(Const("🏠 Главное меню"), id="back_menu_btn_4", on_click=on_back_menu),
            Button(Const("⏪ Назад"), id="back_btn_4", on_click=on_back),
        ),
        state=Quiz.flat_expire
    ),
    Window(
        Const(text="<b>Как чувствуешь себя в рампе?</b>"),
        Column(
            Button(Const("Ничего не умею"), id="ans_1", on_click=on_answer),
            Button(Const("Раскатка и развороты"), id="ans_2", on_click=on_answer),
            Button(Const("Один / несколько трюков"), id="ans_3", on_click=on_answer),
            Button(Const("5-15 базовых трюков"), id="ans_4", on_click=on_answer),
            Button(Const("15-30 трюков"), id="ans_7", on_click=on_answer),
            Button(Const("Более 30 трюков"), id="ans_10", on_click=on_answer),
            Button(Const("🏠 Главное меню"), id="back_menu_btn_5", on_click=on_back_menu),
            Button(Const("⏪ Назад"), id="back_btn_5", on_click=on_back),
        ),
        state=Quiz.ramp_expire
    ),
    Window(
        Const(text="<b>По грани и/или периле скользишь?</b>"),
        Column(
            Button(Const("Нет / не знаю"), id="ans_1", on_click=on_finish),
            Button(Const("Изучаю скольжения"), id="ans_3", on_click=on_finish),
            Button(Const("Умею 5-10"), id="ans_5", on_click=on_finish),
            Button(Const("Умею 10-15"), id="ans_7", on_click=on_finish),
            Button(Const("Умею больше 15-ти"), id="ans_10", on_click=on_finish),
            Button(Const("🏠 Главное меню"), id="back_menu_btn_6", on_click=on_back_menu),
            Button(Const("⏪ Назад"), id="back_btn_6", on_click=on_back),
        ),
        state=Quiz.rail
    )
)

@quiz.callback_query(F.data == "start_quiz")
async def quiz_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(Quiz.how_much, mode=StartMode.RESET_STACK)
