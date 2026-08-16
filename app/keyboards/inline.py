from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подарить подписку", callback_data="gift")],
        [InlineKeyboardButton(text="Админы", callback_data="admins"),
         InlineKeyboardButton(text="Тарифы", callback_data="tariffs")],
        [InlineKeyboardButton(text="Разделы", callback_data="figures"),
         InlineKeyboardButton(text="Темы", callback_data="tricks")],
        [InlineKeyboardButton(text="Уровни катания", callback_data="levels"),
         InlineKeyboardButton(text="Курсы", callback_data="courses")],
    ]
)

trick_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Сделать бесплатным", callback_data="free")],
        [InlineKeyboardButton(text="⏪ Назад", callback_data="back")]
    ]
)

start_quiz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👉🏻 Начать", callback_data="start_quiz")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="user_back")]
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="back")]
    ]
)

skip_video = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Пропустить", callback_data="video_skip")],
        [InlineKeyboardButton(text="Отмена", callback_data="back")]
    ]
)

user_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="user_back")]
    ]
)

user_back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="user_back_menu")]
    ]
)

free_lesson_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="free_yes"),
         InlineKeyboardButton(text="❌ Нет", callback_data="free_no")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=config.bot.channel_link)],
        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]
    ]
)
