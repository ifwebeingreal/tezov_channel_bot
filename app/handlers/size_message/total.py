from aiogram.types import CallbackQuery
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb


async def total_size(callback: CallbackQuery, total: int):
    if 3 <= total <= 4:
        await callback.message.edit_text(
            """Вам подойдет размер доски шириной 7.6, 7.7 дюймов. Да, в магазинах чаще всего размер доски указан именно в дюймах☝️""",
            reply_markup=ikb.user_back
        )

    elif 5 <= total <= 9:
        await callback.message.edit_text(
            """Вам подойдет размер доски шириной 8.0, 8.1 дюймов. Да, в магазинах чаще всего размер доски указан именно в дюймах☝️""",
            reply_markup=ikb.user_back
        )

    elif 10 <= total <= 13:
        await callback.message.edit_text(
            """Вам подойдет размер доски шириной 8.25, 8.3 дюймов. Да, в магазинах чаще всего размер доски указан именно в дюймах☝️""",
            reply_markup=ikb.user_back
        )

    elif 14 <= total <= 15:
        await callback.message.edit_text(
            """Вам подойдет размер доски шириной 8.5, 8.6 дюймов. Да, в магазинах чаще всего размер доски указан именно в дюймах☝️""",
            reply_markup=ikb.user_back
        )

    elif 16 <= total <= 17:
        await callback.message.edit_text(
            """Вам подойдет размер доски шириной 8.7 - 9.0 дюймов. Да, в магазинах чаще всего размер доски указан именно в дюймах☝️""",
            reply_markup=ikb.user_back
        )
    else:
        await callback.message.answer(f"<b>Результат {total}</b> — вне диапазона уровней.")
