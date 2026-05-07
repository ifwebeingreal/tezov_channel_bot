from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin.select import get_admins
from app.database.requests.figure.select import get_figures_by_level_id
from app.database.requests.skate_level.select import get_skate_levels
from app.database.requests.tariff.select import get_tariffs
from app.database.requests.subscription.select import get_subscription
from app.database.requests.trick.select import get_tricks_by_level_id_and_figure_id, get_trick_by_id
from app.database.requests.course.select import get_courses
from app.database.requests.lesson.select import get_lessons_by_course_id, get_free_lessons, get_not_free_lessons


async def admins_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"))

    admins = await get_admins()
    for admin in admins:
        kb.row(InlineKeyboardButton(text=f"{admin.tg_id}", callback_data=f"admin_{admin.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_admin(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deleteadmin_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"admins"))

    return kb.as_markup()


async def tariffs_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить тариф", callback_data="add_tariff"))

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.name}", callback_data=f"tariff_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_tariff(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"editname_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить стоимость", callback_data=f"editprice_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить количество дней", callback_data=f"editdayscount_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deletetariff_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"tariffs"))

    return kb.as_markup()


async def user_panel(tg_id):
    kb = InlineKeyboardBuilder()

    courses = await get_courses()

    for course in courses:
        kb.row(InlineKeyboardButton(text=f"{course.title}", callback_data=f"usercourse_{course.id}"))

    # subscription = await get_subscription(tg_id=tg_id)
    #
    # if subscription:
    #     kb.row(InlineKeyboardButton(text="Продлить подписку", callback_data="extend_subscription"))
    #     if subscription and subscription.is_active:
    #         kb.row(InlineKeyboardButton(text="❌ Отключить автосписание", callback_data="cancel_subscription"))
    #     else:
    #         kb.row(InlineKeyboardButton(text="✅ Включить автосписание", callback_data="activate_subscription"))
    # else:
    #     kb.row(InlineKeyboardButton(text="Тарифы", callback_data="all_tariffs"))

    # kb.row(InlineKeyboardButton(text="Мастерская", callback_data="channel"))
    kb.row(InlineKeyboardButton(text="База знаний", callback_data="skate_base"))
    kb.row(InlineKeyboardButton(text="Узнать свой уровень", callback_data="check_level"))

    return kb.as_markup()


async def channel_panel(tg_id):
    kb = InlineKeyboardBuilder()

    subscription = await get_subscription(tg_id=tg_id)

    if subscription:
        kb.row(InlineKeyboardButton(text="Продлить подписку", callback_data="extend_subscription"))
        if subscription and subscription.is_active:
            kb.row(InlineKeyboardButton(text="❌ Отключить автосписание", callback_data="cancel_subscription"))
        else:
            kb.row(InlineKeyboardButton(text="✅ Включить автосписание", callback_data="activate_subscription"))
    else:
        kb.row(InlineKeyboardButton(text="Тарифы", callback_data="all_tariffs"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="user_back"))

    return kb.as_markup()


async def user_back_menu_and_pay(tg_id):
    kb = InlineKeyboardBuilder()

    subscription = await get_subscription(tg_id=tg_id)

    if subscription:
        kb.row(InlineKeyboardButton(text="Присоединиться", callback_data="extend_subscription"))
    else:
        kb.row(InlineKeyboardButton(text="Присоединиться", callback_data="all_tariffs"))

    kb.row(InlineKeyboardButton(text="Вернуться в меню", callback_data="user_back_menu"))

    return kb.as_markup()


async def user_tariffs_cb():
    kb = InlineKeyboardBuilder()

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.name}", callback_data=f"usertariff_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="channel"))

    return kb.as_markup()


async def user_extend_cb():
    kb = InlineKeyboardBuilder()

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.name}", callback_data=f"userextend_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="channel"))

    return kb.as_markup()


async def ukassa_pay(url):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Оплатить", url=url))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="channel"))

    return kb.as_markup()


async def ukassa_pay_course(url):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Оплатить", url=url))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"user_back"))

    return kb.as_markup()


async def gift_tariffs_cb():
    kb = InlineKeyboardBuilder()

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.name}", callback_data=f"gifttariff_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def levels_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить уровень", callback_data="add_level"))

    levels = await get_skate_levels()
    for level in levels:
        kb.row(InlineKeyboardButton(text=f"{level.name}", callback_data=f"level_{level.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_level(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить", callback_data=f"editlvl_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deletelvl_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"levels"))

    return kb.as_markup()


async def figure_levels_cb():
    kb = InlineKeyboardBuilder()

    levels = await get_skate_levels()
    for level in levels:
        kb.row(InlineKeyboardButton(text=f"{level.name}", callback_data=f"flevel_{level.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def figure_cb(level_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить фигуру", callback_data=f"add_figure_{level_id}"))

    figures = await get_figures_by_level_id(level_id)
    for figure in figures:
        kb.row(InlineKeyboardButton(text=f"{figure.name}", callback_data=f"figure_{figure.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"figures"))

    return kb.as_markup()


async def edit_figure(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить", callback_data=f"editfig_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deletefig_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"figures"))

    return kb.as_markup()


async def trick_levels_cb():
    kb = InlineKeyboardBuilder()

    levels = await get_skate_levels()
    for level in levels:
        kb.row(InlineKeyboardButton(text=f"{level.name}", callback_data=f"tlevel_{level.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def trick_figure_cb(level_id):
    kb = InlineKeyboardBuilder()

    figures = await get_figures_by_level_id(level_id)
    for figure in figures:
        kb.row(InlineKeyboardButton(text=f"{figure.name}", callback_data=f"tfigure_{figure.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"back"))

    return kb.as_markup()


async def trick_cb(level_id, figure_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить трюк", callback_data=f"add_trick_{level_id}_{figure_id}"))

    tricks = await get_tricks_by_level_id_and_figure_id(level_id, figure_id)
    for trick in tricks:
        kb.row(InlineKeyboardButton(text=f"{trick.name}", callback_data=f"trick_{trick.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"back"))

    return kb.as_markup()


async def edit_trick(id):
    kb = InlineKeyboardBuilder()

    trick = await get_trick_by_id(id)

    kb.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"edittrick_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить описание", callback_data=f"edittrickdesc_{id}"))
    if trick.video:
        kb.row(InlineKeyboardButton(text="❌ Удалить видео", callback_data=f"deletevideo_{id}"))
        kb.row(InlineKeyboardButton(text="✏️ Изменить видео", callback_data=f"edittrickvideo_{id}"))
    else:
        kb.row(InlineKeyboardButton(text="➕ Добавить видео", callback_data=f"edittrickvideo_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить цену", callback_data=f"edittrickprice_{id}"))
    if trick.price:
        kb.row(InlineKeyboardButton(text="🎁 Сделать бесплатным", callback_data=f"edittrickfree_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deletetrick_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"tricks"))

    return kb.as_markup()


async def courses_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить курс", callback_data=f"add_course"))

    courses = await get_courses()

    for course in courses:
        kb.row(InlineKeyboardButton(text=f"{course.title}", callback_data=f"course_{course.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"back"))

    return kb.as_markup()


async def edit_course(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✉️ Уроки", callback_data=f"lessons_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"edit_course_title_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить описание", callback_data=f"edit_course_desc_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить стоимость", callback_data=f"edit_course_price_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить видео", callback_data=f"edit_course_video_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_course_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"courses"))

    return kb.as_markup()


async def lessons_cb(course_id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить урок", callback_data=f"add_lesson_{course_id}"))

    lessons = await get_lessons_by_course_id(course_id)

    for lesson in lessons:
        kb.row(InlineKeyboardButton(text=f"{lesson.title}", callback_data=f"lesson_{lesson.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"course_{course_id}"))

    return kb.as_markup()


async def edit_lesson(id: int, is_free: bool, course_id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"edit_lesson_title_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить описание", callback_data=f"edit_lesson_desc_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить видео", callback_data=f"edit_lesson_video_{id}"))
    if is_free:
        kb.row(InlineKeyboardButton(text="✏️ Сделать платным", callback_data=f"edit_lesson_paid_{id}"))
    else:
        kb.row(InlineKeyboardButton(text="✏️ Сделать бесплатным", callback_data=f"edit_lesson_free_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_lesson_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"lessons_{course_id}"))

    return kb.as_markup()


async def user_course(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Купить", callback_data=f"user_buy_course_{id}"))
    kb.row(InlineKeyboardButton(text="Бесплатный контент", callback_data=f"user_check_free_{id}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data=f"user_back"))

    return kb.as_markup()


async def free_lessons_for_user(course_id: int):
    kb = InlineKeyboardBuilder()

    lessons = await get_free_lessons(course_id)

    for lesson in lessons:
        kb.row(InlineKeyboardButton(text=f"{lesson.title}", callback_data=f"freeuserlesson_{lesson.id}"))

    kb.row(InlineKeyboardButton(text="Пройти тест", callback_data="lessons_quiz"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data=f"usercourse_{course_id}"))

    return kb.as_markup()


async def user_back_to_free(course_id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Назад", callback_data=f"user_check_free_{course_id}"))

    return kb.as_markup()


async def no_free_lessons_for_user(course_id: int):
    kb = InlineKeyboardBuilder()

    lessons = await get_not_free_lessons(course_id)

    for lesson in lessons:
        kb.row(InlineKeyboardButton(text=f"{lesson.title}", callback_data=f"userlesson_{lesson.id}"))

    kb.row(InlineKeyboardButton(text="Пройти тест", callback_data="lessons_quiz"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data=f"usercourse_{course_id}"))

    return kb.as_markup()


async def user_back_to_no_free(course_id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Задать вопрос", url="https://t.me/DanyaTezov"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data=f"user_buy_course_{course_id}"))

    return kb.as_markup()