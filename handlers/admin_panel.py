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

@admin_router.message(F.text=='⚙️ Админ панель') #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    await message.answer("Что делаем?:", reply_markup=admin_buttons())
    await state.set_state(Form.admin)
@admin_router.message(F.text == 'Норма часы всех',Form.admin)  # НАЧАЛО
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
    if message.text == "Выбрать диапазон":
        await message.answer("Введите диапазон в формате: гггг-мм-дд >> гггг-мм-дд")
        await state.set_state(Form.get_norm_diapazon_admin)
    if message.text == "❌ Отмена":
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                   reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)


@admin_router.message(F.text, Form.get_norm_diapazon_admin)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                   reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)
    dates = message.text.split(' >> ')
    print(dates)
    await state.set_state(Form.client_start)
    await message.answer(await get_times_all(dates[0],dates[1]))

    await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                               caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                               reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
@admin_router.message(F.text == 'Использованные зч',Form.admin)  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    if await get_lost_spares():
        await message.answer("Использованные запчасти:", reply_markup=main_kb(message.from_user.id))
        document = FSInputFile('temporary_folder/lost_spares1.xlsx')
        await bot.send_document(message.chat.id, document)
        document = FSInputFile('temporary_folder/lost_pares2.xlsx')
        await bot.send_document(message.chat.id, document)
    await state.set_state(Form.client_start)
@admin_router.message(F.text == 'Все работы',Form.admin)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await export_collections_to_xlsx()
    await message.answer("Использованные запчасти:", reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
    document = FSInputFile('temporary_folder/electro.xlsx')
    await bot.send_document(message.chat.id, document)
    document = FSInputFile('temporary_folder/mechanical.xlsx')
    await bot.send_document(message.chat.id, document)
    document = FSInputFile('temporary_folder/akb.xlsx')
    await bot.send_document(message.chat.id, document)
