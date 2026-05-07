import datetime
from operator import itemgetter

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Column, Button, ScrollingGroup, Select, Url, Row, PrevPage, NextPage, Group
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.user.add import set_user
from app.database.requests.admin.select import get_admins

from app.states import UserSG

from app.handlers.user_dialog.getters import (skate_levels_getter, figures_getter,
                                              tricks_getter, trick_info_getter, payment_getter, prefix_tricks_getter)

from app.handlers.user_dialog.onclick import (on_skate_level, on_back,
                                              on_back_menu, on_figure,
                                              on_trick, on_trick_info,
                                              on_back_2, on_one_list,
                                              on_nine_in_one, on_trick_2)

from app.handlers.user_dialog.text_input import correct_search_tricks, check_text


user = Router()


MAIN_TEXT = """База знаний - это библиотека трюков и элементов. Каждое отдельное видео - компактная шпаргалка с поэтапным изучением движения☝️

Выбери уровень подготовки, раздел, трюк, и скорее иди применять полученные знания на практике💪"""


user_dialog = Dialog(
    Window(
        Format(MAIN_TEXT),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="skate_levels",
                item_id_getter=itemgetter(1),
                on_click=on_skate_level,
            ),
            width=1,
            height=3,
            id="skate_level_scroll",
            hide_pager=True,
        ),
        Row(
            PrevPage(scroll="skate_level_scroll", text=Const("⬅️")),
            NextPage(scroll="skate_level_scroll", text=Const("➡️")),
        ),
        Column(
            Button(Const("🏡 Назад в меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=UserSG.skate_level,
        getter=skate_levels_getter,
    ),
    Window(
        Format("{text}"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="figures",
                item_id_getter=itemgetter(1),
                on_click=on_figure
            ),
            width=1,
            height=3,
            id="figure_list",
            hide_pager=True,
        ),
        Row(
            PrevPage(scroll="figure_list", text=Const("⬅️")),
            NextPage(scroll="figure_list", text=Const("➡️")),
        ),
        Column(
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
        ),
        state=UserSG.figure,
        getter=figures_getter,
    ),
    Window(
        Const(text="<b>Выберите отображение тем или трюков</b>"),
        Column(
            Button(Const("Списком"), id="one_list", on_click=on_one_list),
            Button(Const("По 9 шт."), id="nine_in_one", on_click=on_nine_in_one),
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
        ),
        state=UserSG.select_visual
    ),
    Window(
        Const("<b>Выбери тему:</b>"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="tricks",
                item_id_getter=itemgetter(1),
                on_click=on_trick_2,
            ),
            width=1,
            height=9,
            id="trick_list",
            hide_pager=True,
            when="visual"
        ),
        Row(
            PrevPage(scroll="trick_list", text=Const("⬅️")),
            NextPage(scroll="trick_list", text=Const("➡️")),
            when="visual"
        ),
        TextInput(
            id="waiting_for_name",
            type_factory=check_text,
            on_success=correct_search_tricks
        ),
    Column(
        Select(
            Format("{item[0]}"),
            id="ms_plain",
            items="tricks",
            item_id_getter=itemgetter(1),
            on_click=on_trick_2,
        ),
        when=lambda data, widget, manager: not data.get("visual")
    ),
        Column(
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Назад в меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=UserSG.tricks,
        getter=tricks_getter,
    ),
    Window(
Const("<b>Выбери тему:</b>"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="tricks_by_prefix",
                item_id_getter=itemgetter(1),
                on_click=on_trick,
            ),
            width=1,
            height=9,
            id="prefix_trick_list",
            hide_pager=True,
            when="visual"
        ),
        Row(
            PrevPage(scroll="prefix_trick_list", text=Const("⬅️")),
            NextPage(scroll="prefix_trick_list", text=Const("➡️")),
            when="visual"
        ),
    Column(
        Select(
            Format("{item[0]}"),
            id="ms_plain",
            items="tricks_by_prefix",
            item_id_getter=itemgetter(1),
            on_click=on_trick,
        ),
        when=lambda data, widget, manager: not data.get("visual")
    ),
        Column(
            Button(Const("⏪ Назад"), id="back", on_click=on_back),
            Button(Const("🏡 Назад в меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=UserSG.searched_tricks,
        getter=prefix_tricks_getter,
    ),
    Window(
DynamicMedia("video", when="video"),
        Const("<b>Информация о  видео:</b>\n"),
        Format("{name}\n"),
        Format("{description}\n"),
        Column(
            Button(Const("⏪ Назад"), id="back", on_click=on_back_2),
            Button(Const("🏡 Назад в меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=UserSG.trick_info,
        getter=trick_info_getter,
    ),
    Window(
        Format(
            text="Для того, чтобы получить доступ к теме <b>{name}</b>, необходимо оплатить <b>{price}</b> руб."
        ),
        Column(
            Url(text=Format('💰 Оплатить'), url=Format('{payment_url}'), id='button_2'),
            Button(Const("⏪ Назад"), id="back", on_click=on_back_2),
            Button(Const("🏡 Назад в меню"), id="back_menu", on_click=on_back_menu),
        ),
        state=UserSG.pay_menu,
        getter=payment_getter
    )
)


@user.callback_query(F.data == "skate_base")
async def skate_base_callback(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserSG.skate_level, mode=StartMode.RESET_STACK)



