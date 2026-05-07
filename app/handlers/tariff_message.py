from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.tariff.add import set_tariff
from app.database.requests.tariff.select import get_tariffs, get_tariff
from app.database.requests.tariff.update import (update_tariff_price, update_tariff_nane,
                                                 update_tariff_days_count)
from app.database.requests.tariff.delete import delete_tariff

from app.states import AddTariff, EditTariff


tariff = Router()


@tariff.callback_query(F.data == "tariffs")
async def tariffs_menu(callback: CallbackQuery):
    await callback.message.edit_text("<b>Добавленные тарифы:</b>",
                                     reply_markup=await bkb.tariffs_cb())


@tariff.callback_query(F.data == "add_tariff")
async def add_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Введите название тарифа:</b>",
                                     reply_markup=ikb.admin_cancel)
    await state.set_state(AddTariff.name)


@tariff.message(AddTariff.name)
async def add_tariff_name(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 300:
        await state.update_data(name=message.text)
        await message.answer("<b>Введите стоимость тарифа:</b>",
                             reply_markup=ikb.admin_cancel)
        await state.set_state(AddTariff.price)
    else:
        await message.answer("<b>Название тарифа должно содержать не более 300 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@tariff.message(AddTariff.price)
async def add_tariff_price(message: Message, state: FSMContext):
    price_text = message.text.replace(",", ".").strip()

    try:
        price = float(price_text)
        if price <= 0:
            raise ValueError

        await state.update_data(price=price)
        await message.answer("<b>Введите количество дней тарифа:</b>",
                             reply_markup=ikb.admin_cancel)

        await state.set_state(AddTariff.days_count)

    except ValueError:
        await message.answer(
            "<b>Введите корректную цену — только число (например, 1000, 1000.00 или 1000,50).</b>",
            reply_markup=ikb.admin_cancel
        )


@tariff.message(AddTariff.days_count)
async def add_tariff_days_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(days_count=int(message.text))
        data = await state.get_data()

        name = data.get("name")
        price = data.get("price")
        days_count = data.get("days_count")

        await set_tariff(name=name,
                         price=price,
                         days_count=days_count)

        await message.answer("<b>Тариф успешно добавлен!</b>",
                             reply_markup=await bkb.tariffs_cb())

        await state.clear()
    else:
        await message.answer("<b>Количество дней должно быть целым положительным числом!</b>",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("tariff_"))
async def tariff_info_panel(callback: CallbackQuery):
    tariff_id = int(callback.data.split("_")[1])
    tariff_info = await get_tariff(tariff_id)

    await callback.message.edit_text(f"<b>Панель управления тарифом:</b>\n\n"
                                     f"<b>Название:</b> {tariff_info.name}\n"
                                     f"<b>Цена:</b> {tariff_info.price}\n"
                                     f"<b>Количество дней:</b> {tariff_info.days_count}\n\n"
                                     f"<b><i>Выберите действие:</i></b>",
                                     reply_markup=await bkb.edit_tariff(tariff_id))


@tariff.callback_query(F.data.startswith("editname_"))
async def edit_tariff_name(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(tariff_id=tariff_id)
    await callback.message.edit_text("<b>Введите новое название тарифа:</b>",
                                     reply_markup=ikb.admin_cancel)
    await state.set_state(EditTariff.name)


@tariff.message(EditTariff.name)
async def edit_tariff_name(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 300:
        await state.update_data(name=message.text)
        data = await state.get_data()
        tariff_id = data.get("tariff_id")
        name = data.get("name")

        await update_tariff_nane(tariff_id, name)

        tariff_info = await get_tariff(tariff_id)

        await message.answer(f"<b>Панель управления тарифом:</b>\n\n"
                                         f"<b>Название:</b> {tariff_info.name}\n"
                                         f"<b>Цена:</b> {tariff_info.price}\n"
                                         f"<b>Количество дней:</b> {tariff_info.days_count}\n\n"
                                         f"<b><i>Выберите действие:</i></b>",
                                         reply_markup=await bkb.edit_tariff(tariff_id))
        await state.clear()
    else:
        await message.answer("<b>Название тарифа должно содержать не более 300 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("editprice_"))
async def edit_tariff_price(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(tariff_id=tariff_id)
    await callback.message.edit_text("<b>Введите новую цену тарифа:</b>",
                                     reply_markup=ikb.admin_cancel)
    await state.set_state(EditTariff.price)


@tariff.message(EditTariff.price)
async def edit_tariff_price(message: Message, state: FSMContext):
    price_text = message.text.replace(",", ".").strip()

    try:
        price = float(price_text)
        if price <= 0:
            raise ValueError

        await state.update_data(price=price)
        data = await state.get_data()
        tariff_id = data.get("tariff_id")
        price = data.get("price")

        await update_tariff_price(tariff_id, price)

        tariff_info = await get_tariff(tariff_id)

        await message.answer(f"<b>Панель управления тарифом:</b>\n\n"
                                         f"<b>Название:</b> {tariff_info.name}\n"
                                         f"<b>Цена:</b> {tariff_info.price}\n"
                                         f"<b>Количество дней:</b> {tariff_info.days_count}\n\n"
                                         f"<b><i>Выберите действие:</i></b>",
                                         reply_markup=await bkb.edit_tariff(tariff_id))

        await state.clear()

    except ValueError:
        await message.answer(
            "<b>Введите корректную цену — только число (например, 1000, 1000.00 или 1000,50).</b>",
            reply_markup=ikb.admin_cancel
        )


@tariff.callback_query(F.data.startswith("editdayscount_"))
async def edit_tariff_days_count(callback: CallbackQuery, state: FSMContext):
    tariff_id = int(callback.data.split("_")[1])
    await state.update_data(tariff_id=tariff_id)
    await callback.message.edit_text("<b>Введите новое количество дней:</b>",
                                     reply_markup=ikb.admin_cancel)
    await state.set_state(EditTariff.days_count)


@tariff.message(EditTariff.days_count)
async def edit_tariff_days_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(days_count=int(message.text))
        data = await state.get_data()
        tariff_id = data.get("tariff_id")
        days_count = data.get("days_count")

        await update_tariff_days_count(tariff_id, days_count)

        tariff_info = await get_tariff(tariff_id)

        await message.answer(f"<b>Панель управления тарифом:</b>\n\n"
                                         f"<b>Название:</b> {tariff_info.name}\n"
                                         f"<b>Цена:</b> {tariff_info.price}\n"
                                         f"<b>Количество дней:</b> {tariff_info.days_count}\n\n"
                                         f"<b><i>Выберите действие:</i></b>",
                                         reply_markup=await bkb.edit_tariff(tariff_id))

        await state.clear()
    else:
        await message.answer("<b>Введите корректное количество дней!</b>",
                             reply_markup=ikb.admin_cancel)


@tariff.callback_query(F.data.startswith("deletetariff_"))
async def remove_tariff(callback: CallbackQuery):
    tariff_id = int(callback.data.split("_")[1])
    await delete_tariff(tariff_id)

    await callback.message.edit_text("<b>Тариф успешно удален!</b>",
                                     reply_markup=await bkb.tariffs_cb())