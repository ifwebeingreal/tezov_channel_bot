from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    tg_id = State()


class AddTariff(StatesGroup):
    name = State()
    price = State()
    days_count = State()


class EditTariff(StatesGroup):
    name = State()
    price = State()
    days_count = State()


class Gift(StatesGroup):
    tariff_id = State()
    tg_id = State()


class Quiz(StatesGroup):
    how_much = State()
    figures = State()
    returns = State()
    flat_expire = State()
    ramp_expire = State()
    rail = State()


class AddLevel(StatesGroup):
    name = State()

    new_name = State()


class AddFigure(StatesGroup):
    name = State()

    new_name = State()


class CheckTrick(StatesGroup):
    level_id = State()
    figure_id = State()


class AddTrick(StatesGroup):
    name = State()
    description = State()
    video = State()
    price = State()

    new_name = State()
    new_description = State()
    new_video = State()
    new_price = State()


class UserSG(StatesGroup):
    skate_level = State()
    figure = State()
    select_visual = State()
    tricks = State()
    searched_tricks = State()
    trick_info = State()
    pay_menu = State()


class AddCourse(StatesGroup):
    title = State()
    description = State()
    price = State()
    video = State()


class UpdateCourse(StatesGroup):
    new_title = State()
    new_description = State()
    new_price = State()
    new_video = State()


class AddLesson(StatesGroup):
    title = State()
    description = State()
    video = State()
    is_free = State()


class UpdateLesson(StatesGroup):
    new_title = State()
    new_description = State()
    new_video = State()
    is_free = State()