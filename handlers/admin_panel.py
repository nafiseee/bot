from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from create_bot import Form
from create_bot import bot
from db_handler.db_class import get_times_all, get_lost_spares, export_collections_to_xlsx
from keyboards.all_kb import main_kb, admin_buttons

admin_router = Router()
from datetime import datetime
from keyboards.all_kb import norm_times_menu

# Импортируем тексты и кнопки
from texts import *
from buttons import *

@admin_router.message(F.text == BUTTON_ADMIN_PANEL)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    await message.answer(TEXT_ADMIN_QUESTION, reply_markup=admin_buttons())
    await state.set_state(Form.admin)

@admin_router.message(F.text == BUTTON_NORM_HOURS_ALL, Form.admin)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end_of_month = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        end_of_month = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
    start_str = start_of_month.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_of_month.strftime("%Y-%m-%d %H:%M:%S")

    await message.answer(
        f"{await get_times_all()}", reply_markup=norm_times_menu())
    await state.set_state(Form.norm_times_menu_admin)


@admin_router.message(F.text, Form.norm_times_menu_admin)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == BUTTON_SELECT_RANGE:
        await message.answer(TEXT_ENTER_DATE_RANGE)
        await state.set_state(Form.get_norm_diapazon_admin)
    if message.text == BUTTON_CANCEL:
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
        await state.set_state(Form.client_start)


@admin_router.message(F.text, Form.get_norm_diapazon_admin)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == BUTTON_CANCEL:
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
        await state.set_state(Form.client_start)
    dates = message.text.split(' >> ')
    print(dates)
    await state.set_state(Form.client_start)
    await message.answer(await get_times_all(dates[0], dates[1]))

    await message.answer_photo(
        photo=FSInputFile('media/1.jpg', filename='Снеговик'),
        caption=TEXT_MAIN_MENU,
        reply_markup=main_kb(message.from_user.id)
    )
    await state.set_state(Form.client_start)

@admin_router.message(F.text == BUTTON_USED_SPARES, Form.admin)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    if await get_lost_spares():
        await message.answer(TEXT_USED_SPARES, reply_markup=main_kb(message.from_user.id))
        document = FSInputFile('temporary_folder/lost_spares1.xlsx')
        await bot.send_document(message.chat.id, document)
        document = FSInputFile('temporary_folder/lost_spares2.xlsx')
        await bot.send_document(message.chat.id, document)
    await state.set_state(Form.client_start)

@admin_router.message(F.text == BUTTON_ALL_WORKS, Form.admin)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await export_collections_to_xlsx()
    await message.answer(TEXT_USED_SPARES, reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
    document = FSInputFile('temporary_folder/electro.xlsx')
    await bot.send_document(message.chat.id, document)
    document = FSInputFile('temporary_folder/mechanical.xlsx')
    await bot.send_document(message.chat.id, document)
    document = FSInputFile('temporary_folder/akb.xlsx')
    await bot.send_document(message.chat.id, document)
    document = FSInputFile('bot_debug.log')
    await bot.send_document(message.chat.id, document)