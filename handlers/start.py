from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from keyboards.all_kb import main_kb, b_models, works_edit_kb, m_or_e_kb, edit_work, iots_pred, cancel, norm_times_menu, akt_zero
from aiogram.utils.chat_action import ChatActionSender
from validators.validators import name_validate, phone_validate, act_validate, model_validate, id_validate, iot_validate, bycycle_type_validate
from datetime import timedelta
import pandas as pd
from utils.info import info
from db_handler import db_class
from db_handler.db_class import get_my_time
from create_bot import Form
from db_handler.db_class import check_sub, add_user, get_user_name, find_remont, get_pred_iot, delete_remont, get_act_ids
from aiogram.exceptions import TelegramBadRequest
from create_bot import bot
from decouple import config

# Импортируем тексты и кнопки
from texts import *
from buttons import *

start_photo = FSInputFile('media/sticker.webm', filename='хуй')
client_work_keys = ['work_type', 'full_name', 'phone_number', 'act_id', 'b_model', 'b_id', 'iot_id']
client_work = ['', '', 'Номер телефона: ', 'Акт №', 'Модель велосипеда: ', 'Номер велосипеда: ', 'IoT: ']

start = Router()
questionnaire_router = Router()
works_router = Router()
df = pd.read_excel('works_norm.xlsx', names=['work', 'time', 'type', 'sale', 'group'])
print('таблица открыта')

async def init_work(state, message):
    print('инициализя')
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    await state.update_data(employer_name=await get_user_name(message.from_user.id), user_id=message.from_user.id)
    await message.answer(await info(state), reply_markup=works_edit_kb())
    await state.set_state(Form.next_menu)

@questionnaire_router.message(F.text == BUTTON_CANCEL, Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('Отмена add_spare_')
    await state.set_state(Form.next_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())

@questionnaire_router.message(F.text == BUTTON_CANCEL, Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.set_state(Form.akb_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())

@questionnaire_router.message(F.text == BUTTON_CANCEL_REPAIR, Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
    await state.set_state(Form.client_start)

@questionnaire_router.message(F.text == BUTTON_CANCEL_REPAIR, Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
    await state.set_state(Form.client_start)

@questionnaire_router.message(F.text == BUTTON_NORM_HOURS_USER)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer(f"{await get_my_time(message.from_user.id)}", reply_markup=norm_times_menu())
    await state.set_state(Form.norm_times_menu)

@questionnaire_router.message(F.text, Form.norm_times_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == BUTTON_SELECT_RANGE:
        await message.answer(TEXT_ENTER_DATE_RANGE)
        await state.set_state(Form.get_norm_diapazon)
    if message.text == BUTTON_CANCEL:
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
        await state.set_state(Form.client_start)

@questionnaire_router.message(F.text, Form.get_norm_diapazon)
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
    await message.answer(f"{str(await get_my_time(message.from_user.id, dates[0], dates[1]))}")
    await message.answer_photo(
        photo=FSInputFile('media/1.jpg', filename='Снеговик'),
        caption=TEXT_MAIN_MENU,
        reply_markup=main_kb(message.from_user.id)
    )
    await state.set_state(Form.client_start)

from aiogram.filters import StateFilter

@questionnaire_router.message(F.text == BUTTON_SAVE_REPAIR, StateFilter(Form.next_menu, Form.akb_menu))
async def start_questionnaire_process(message: Message, state: FSMContext):

    print("Сохранить ремонт next_menu")
    await state.update_data(end_time=(timedelta(hours=3) + message.date).strftime("%Y-%m-%d %H:%M:%S"))
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        msg = await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
    await state.set_state(Form.client_start)
    data = await state.get_data()
    if '_id' in data:
        print('есть _id')
        print(data['end_time'])
        try:
            await bot.edit_message_text(
                chat_id=config('CHAT_ID'),
                message_id=int(data['msg_id']),
                text=await info(state))
        except TelegramBadRequest:
            bot.delete_message(chat_id=config('CHAT_ID'), message_id=int(data['msg_id']))
            print('сохраняем ремонт')
            m_or_e = await state.get_data()['m_or_e']
            print(m_or_e, 'fffff f')
            if m_or_e:
                if m_or_e=='Электро':
                    message = await bot.send_message(config('CHAT_ID'), await info(state), reply_to_message_id=config('ELECTRO_TOPIC_ID'))
                else:
                    message = await bot.send_message(config('CHAT_ID'), await info(state),reply_to_message_id=config('MECHANICAL_TOPIC_ID'))
            else:
                message = await bot.send_message(config('CHAT_ID'), await info(state), reply_to_message_id=config('AKB_TOPIC_ID'))
            await state.update_data(msg_id=message.message_id)
    else:
        print('сохраняем ремонт')
        if 'm_or_e' in dict(await state.get_data()):
            m_or_e = dict(await state.get_data())['m_or_e']
            if m_or_e=='Электро':
                message = await bot.send_message(config('CHAT_ID'), await info(state), reply_to_message_id=config('ELECTRO_TOPIC_ID'))
            else:
                message = await bot.send_message(config('CHAT_ID'), await info(state), reply_to_message_id=config('MECHANICAL_TOPIC_ID'))
        else:
            message = await bot.send_message(config('CHAT_ID'), await info(state), reply_to_message_id=config('AKB_TOPIC_ID'))
        await state.update_data(msg_id=message.message_id)
    await db_class.save_remont(state)

@start.message(Command("get_ids"))
async def get_ids(message: Message):
    await message.answer(
        f"Chat ID: {message.chat.id}\n"
        f"Topic ID: {message.message_thread_id}"
    )

@start.message(Command('start'))  # НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("старт епта")
    if message.chat.id != config('CHAT_ID'):
        if await check_sub(message.from_user.id):
            await state.clear()
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                await message.answer_photo(
                    photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                    caption=TEXT_MAIN_MENU,
                    reply_markup=main_kb(message.from_user.id)
                )
                await state.set_state(Form.client_start)
        else:
            await message.answer(TEXT_ENTER_NAME, reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.get_name_employer)
    else:
        print('пишут не в бота. поэтому отмена.', message.chat.id)
    print('хуййй')
    print(await state.get_state())

@questionnaire_router.message(F.text, Form.get_name_employer)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("регистрация")
    if name_validate(message.text):
        await add_user(message.from_user.id, message.text)
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
        await state.set_state(Form.client_start)
    else:
        await message.answer(TEXT_INVALID_NAME_RESTART, reply_markup=ReplyKeyboardRemove())

@questionnaire_router.message(F.text == BUTTON_TECH_SERVICE, Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("ТОшка")
    await state.clear()
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=(timedelta(hours=3) + message.date).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await message.answer(TEXT_ENTER_ACT_NUMBER, reply_markup=akt_zero())
    await state.set_state(Form.act_id)

@questionnaire_router.message(F.text == BUTTON_CLIENT_REPAIR, Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Клиентский белэжт")
    await state.clear()
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=(message.date + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await state.update_data(message_id=message.from_user.id + 1)
        await message.answer(TEXT_ENTER_FULL_NAME, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.full_name)

@questionnaire_router.message(F.text == BUTTON_BATTERY, Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Акб")
    await state.clear()
    await state.set_state(Form.act_akb_id)
    await message.answer(TEXT_ENTER_ACT_NUMBER_SHORT, reply_markup=akt_zero())

@questionnaire_router.message(F.text == BUTTON_MUSIC, Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Музыка")
    audio_file1 = FSInputFile("media/1.mp3", "sigma1.mp3")
    audio_file2 = FSInputFile("media/2.mp3", "sigma2.mp3")
    audio_file3 = FSInputFile("media/3.mp3", "sigma3.mp3")
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_audio(audio_file2)
    await message.answer_photo(
        photo=FSInputFile('media/1.jpg', filename='Снеговик'),
        caption=TEXT_MAIN_MENU,
        reply_markup=main_kb(message.from_user.id)
    )
    await state.set_state(Form.client_start)

@questionnaire_router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Имя")
    if not name_validate(message.text):
        await message.reply(TEXT_INVALID_NAME_FORMAT)
        return
    await state.update_data(full_name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(TEXT_ENTER_PHONE, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.phone_number)

@questionnaire_router.message(F.text, Form.phone_number)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Номер телеофна")
    if not phone_validate(message.text):
        await message.reply(TEXT_INVALID_PHONE)
        return
    await state.update_data(phone_number=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(TEXT_ENTER_ACT_NUMBER_SHORT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)

@questionnaire_router.message(F.text, Form.act_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("номер акта")
    if not act_validate(message.text):
        await message.reply(TEXT_INVALID_ACT_NUMBER)
        return
    q = await get_act_ids()
    print(q)
    if message.text in q and message.text not in ['Акт отсутствует', '0']:
        await message.reply(TEXT_ACT_EXISTS)
        return
    await state.update_data(act_id=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(TEXT_CHOOSE_BIKE_TYPE, reply_markup=m_or_e_kb())
    await state.set_state(Form.b_or_e)

@questionnaire_router.message(F.text, Form.b_or_e)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('Вид велика')
    if not bycycle_type_validate(message.text):
        await message.reply(TEXT_INVALID_BIKE_TYPE, reply_markup=m_or_e_kb())
        return
    await state.update_data(m_or_e=message.text.split(' ')[1], user_id=message.from_user.id)
    data = await state.get_data()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer(TEXT_CHOOSE_BIKE_MODEL, reply_markup=b_models(data['m_or_e']))
    await state.set_state(Form.b_model)

@questionnaire_router.message(F.text, Form.b_model)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("модель велика")
    data = await state.get_data()
    if not model_validate(message.text):
        await message.reply(TEXT_CHOOSE_MODEL_FROM_LIST, reply_markup=b_models(data['m_or_e']))
        return
    else:
        await state.update_data(b_model=message.text)
        await message.answer(TEXT_ENTER_BIKE_NUMBER, reply_markup=None)
        await state.set_state(Form.b_id)

@questionnaire_router.message(F.text, Form.b_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('номер велика')
    if not id_validate(message.text):
        await message.reply(TEXT_INVALID_BIKE_NUMBER)
        return
    await state.update_data(b_id=message.text, user_id=message.from_user.id)
    if dict(await state.get_data())['m_or_e'] != 'Механика':
        iots = await get_pred_iot(await state.get_data())
        if iots:
            await message.answer(TEXT_ENTER_IOT_NUMBER, reply_markup=iots_pred(iots))
        else:
            await message.answer(TEXT_ENTER_IOT_NUMBER, reply_markup=None)
        await state.set_state(Form.iot_id)
    else:
        await init_work(state, message)

@questionnaire_router.message(F.text, Form.iot_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("номер иот")
    if '|' in message.text:
        iot_number = message.text.split('|')[1]
    else:
        iot_number = message.text
    if not iot_validate(iot_number):
        await message.reply(TEXT_INVALID_IOT_NUMBER)
        return
    await state.update_data(iot_id=iot_number, user_id=message.from_user.id)
    await init_work(state, message)

@questionnaire_router.message(F.text == BUTTON_EDIT_REPAIR)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('измененеие ремонта [[[')
    await message.reply(TEXT_WHAT_TO_DO_EDIT, reply_markup=edit_work())
    if 'm_or_e' in dict(await state.get_data()):
        await state.set_state(Form.remont_edit)
    else:
        await state.set_state(Form.akb_remont_edit)

@questionnaire_router.message(F.text == BUTTON_EDIT_SAVED_REPAIR)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('измененеие ремонта уже записанного')
    await message.reply(TEXT_FORWARD_REPAIR_TO_EDIT, reply_markup=cancel())
    await state.set_state(Form.saved_remont_edit)

@questionnaire_router.message(F.text, Form.saved_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    if message.text == BUTTON_CANCEL:
        await message.answer_photo(
            photo=FSInputFile('media/1.jpg', filename='Снеговик'),
            caption=TEXT_MAIN_MENU,
            reply_markup=main_kb(message.from_user.id)
        )
        await state.set_state(Form.client_start)
    name, date = message.text.split('\n')[0].split(' | ')
    name = name.split(': ')[1]
    print(await get_user_name(message.from_user.id), name)
    print(message)
    if await get_user_name(message.from_user.id) != name:
        await message.reply(TEXT_NOT_YOUR_REPAIR, reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)
        return

    if 'Номер велосипеда' in message.text:
        a = await find_remont(name, date, 'велик')
    else:
        a = await find_remont(name, date, 'акб')
    await state.clear()
    a['_id'] = str(a['_id'])
    await state.update_data(dict(a))
    await state.update_data(editing_saved=True, user_id=message.from_user.id)
    await state.update_data(message_id=message.message_id, user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    if 'Номер велосипеда' in message.text:
        await state.set_state(Form.next_menu)
    else:
        await state.set_state(Form.akb_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())

@questionnaire_router.message(F.text.contains(TEXT_NO_SPARES_USED))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("ЗАпвчасти не использовались")
    data = await state.get_data()
    if 'akb' in data:
        print('акб')
        await state.set_state(Form.akb_menu)
    else:
        await state.set_state(Form.next_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())