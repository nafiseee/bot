from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile,ReplyKeyboardRemove,CallbackQuery
from keyboards.all_kb import main_kb,b_models,works_edit_kb,m_or_e_kb,edit_work,iots_pred,cancel,norm_times_menu,akt_zero
from aiogram.utils.chat_action import ChatActionSender
from validators.validators import name_validate,phone_validate,act_validate,model_validate,id_validate,iot_validate, bycycle_type_validate
from datetime import timedelta
import pandas as pd
from utils.info import info
from db_handler import db_class
from db_handler.db_class import get_my_time
from create_bot import Form
from db_handler.db_class import check_sub,add_user,get_user_name,find_remont,get_pred_iot,delete_remont
from aiogram.exceptions import TelegramBadRequest
from create_bot import bot

start_photo = FSInputFile('media/sticker.webm', filename='хуй')
client_work_keys = ['work_type','full_name','phone_number','act_id','b_model','b_id','iot_id']
client_work = ['','','Номер телефона: ','Акт №','Модель велосипеда: ','Номер велосипеда: ', 'IoT: ']

start  = Router()
questionnaire_router = Router()
works_router = Router()
df = pd.read_excel('works_norm.xlsx',names = ['work','time','type','sale','group'])
print('таблица открыта')
async def init_work(state,message):
    print('инициализя')
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    await state.update_data(employer_name = await get_user_name(message.from_user.id),user_id=message.from_user.id)
    await message.answer(await info(state), reply_markup=works_edit_kb())
    await state.set_state(Form.next_menu)


@questionnaire_router.message(F.text == "❌ Отмена",Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('Отмена add_spare_')
    await state.set_state(Form.next_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@questionnaire_router.message(F.text == "❌ Отмена",Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.set_state(Form.akb_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())

@questionnaire_router.message(F.text == "Отменить ремонт ❌",Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
                                   reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
@questionnaire_router.message(F.text == "Отменить ремонт ❌",Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
                                   reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
@questionnaire_router.message(F.text == "⏱ Норма-часы")
async def start_questionnaire_process(message: Message, state: FSMContext):
    # now = datetime.now()
    # start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # if now.month == 12:
    #     end_of_month = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # else:
    #     end_of_month = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
    # start_str = start_of_month.strftime("%Y-%m-%d %H:%M:%S")
    # end_str = end_of_month.strftime("%Y-%m-%d %H:%M:%S")

    await message.answer(f"{await get_my_time(message.from_user.id)}",reply_markup=norm_times_menu())
    await state.set_state(Form.norm_times_menu)

@questionnaire_router.message(F.text,Form.norm_times_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == "Выбрать диапазон":
        await message.answer("Введите диапазон в формате: гггг-мм-дд >> гггг-мм-дд")
        await state.set_state(Form.get_norm_diapazon)
    if message.text == "❌ Отмена":
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                   reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)

@questionnaire_router.message(F.text,Form.get_norm_diapazon)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                   reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)
    dates = message.text.split(' >> ')
    print(dates)
    await state.set_state(Form.client_start)
    await message.answer(f"{str(await get_my_time(message.from_user.id,dates[0],dates[1]))}")
    await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                               caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                               reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)

from aiogram.filters import StateFilter
@questionnaire_router.message(F.text == "Сохранить ремонт 💾",StateFilter(Form.next_menu,Form.akb_menu))
async def start_questionnaire_process(message: Message, state: FSMContext):
    f = {'Электро':26,'Механика':34}
    print("Сохранить ремонт next_menu")
    await state.update_data(end_time=(timedelta(hours=3) + message.date).strftime("%Y-%m-%d %H:%M:%S"))
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        msg = await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
                                   reply_markup=main_kb(message.from_user.id))
    # await state.update_data(chat_id=msg.chat.id)
    await state.set_state(Form.client_start)
    data = await state.get_data()
    if '_id' in data:
        print('есть _id')
        print(data['end_time'])
        try:
            await bot.edit_message_text(
                chat_id=-1002979979409,
                message_id=int(data['msg_id']),
                text=await info(state))
        except TelegramBadRequest:
            bot.delete_message(chat_id=-1002979979409,
                message_id=int(data['msg_id']))
            print('сохраняем ремонт')
            m_or_e = await state.get_data()['m_or_e']
            print(m_or_e, 'fffff f')
            if m_or_e:
                message = await bot.send_message(-1002979979409, await info(state), reply_to_message_id=f[m_or_e])
            else:
                message = await bot.send_message(-1002979979409, await info(state), reply_to_message_id=30)
            await state.update_data(msg_id=message.message_id)

    else:
        print('сохраняем ремонт')
        if 'm_or_e' in dict(await state.get_data()):
            m_or_e = dict(await state.get_data())['m_or_e']
            message = await bot.send_message(-1002979979409, await info(state), reply_to_message_id=f[m_or_e])
        else:
            message = await bot.send_message(-1002979979409, await info(state), reply_to_message_id=30)
        await state.update_data(msg_id = message.message_id)
    await db_class.save_remont(state)
# @questionnaire_router.message(F.text == "Сохранить ремонт 💾",Form.akb_menu)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     print("Сохранить ремонт akb_menu")
#     await state.update_data(end_time=(timedelta(hours=3) + message.date).strftime("%Y-%m-%d %H:%M:%S"))
#     async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
#         await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
#                                    caption='Привет я твой помощник по занесению ремонтов. Что будем делать?',
#                                    reply_markup=main_kb(message.from_user.id))
#     await state.set_state(Form.client_start)
#     await bot.send_message(-1002979979409, await info(state), reply_to_message_id=30)
#     await db_class.save_remont(state)
@start.message(Command('start')) #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("старт епта")
    if message.chat.id!=-1002979979409:
        if await check_sub(message.from_user.id):
            await state.clear()
            async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
                await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                           caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                           reply_markup=main_kb(message.from_user.id))
                await state.set_state(Form.client_start)
        else:
            await message.answer('Как тебя звать? [Фамилия Имя] (изменить будет незя)', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.get_name_employer)
    else:
            print('пишут не в бота. поэтому отмена.', message.chat.id)
    print('хуййй')
@questionnaire_router.message(F.text,Form.get_name_employer)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print("регистрация")
    if name_validate(message.text):
        await add_user(message.from_user.id,message.text)
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                    caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                    reply_markup=main_kb(message.from_user.id))

        await state.set_state(Form.client_start)
    else:
        await message.answer('Что-то не так... пробуй заново /start', reply_markup=ReplyKeyboardRemove())
@questionnaire_router.message(F.text=='🛠️ Техническое обслуживание',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("ТОшка")
    await state.clear()
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time = (timedelta(hours=3)+message.date).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await message.answer('Введи номер акта: ', reply_markup=akt_zero())
    await state.set_state(Form.act_id)
@questionnaire_router.message(F.text=='🔧 Клиентский ремонт',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Клиентский белэжт")
    await state.clear()
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=(message.date+timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await state.update_data(message_id = message.from_user.id+1)
        await message.answer('Введи Фамилию Имя:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.full_name)
@questionnaire_router.message(F.text=='🔋 Аккумулятор',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Акб")
    await state.clear()
    await state.set_state(Form.act_akb_id)
    await message.answer("Номер акта:", reply_markup=akt_zero())
@questionnaire_router.message(F.text == '🎵 Музыка', Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Музыка")
    audio_file1 = FSInputFile("media/1.mp3", "sigma1.mp3")
    audio_file2 = FSInputFile("media/2.mp3", "sigma2.mp3")
    audio_file3 = FSInputFile("media/3.mp3", "sigma3.mp3")
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_audio(audio_file2)
    await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                               caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                               reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
@questionnaire_router.message(F.text,Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Имя")
    if not name_validate(message.text):
        await message.reply("Пожалуйста, введите в формате: Фамилия Имя")
        return
    await state.update_data(full_name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введи номер телефона:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.phone_number)
@questionnaire_router.message(F.text,Form.phone_number)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("Номер телеофна")
    if not phone_validate(message.text):
        await message.reply("Пожалуйста введите корректный номер")
        return
    await state.update_data(phone_number=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Номер акта:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
@questionnaire_router.message(F.text,Form.act_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("номер акта")
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_id=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите тип велоиспеда:', reply_markup=m_or_e_kb())
    await state.set_state(Form.b_or_e)
@questionnaire_router.message(F.text,Form.b_or_e)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('Вид велика')
    if not bycycle_type_validate(message.text):
        await message.reply("Некоректный тип велосипеда. Попробуйте заново",reply_markup=m_or_e_kb())
        return
    await state.update_data(m_or_e=message.text.split(' ')[1], user_id=message.from_user.id)
    data = await state.get_data()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите модель велосипеда:', reply_markup=b_models(data['m_or_e']))
    await state.set_state(Form.b_model)
@questionnaire_router.message(F.text,Form.b_model)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("модель велика")
    data = await state.get_data()
    if not model_validate(message.text):
        await message.reply("Выберите модель из списка:",reply_markup=b_models(data['m_or_e']))
        return
    else:
        await state.update_data(b_model=message.text)
        await message.answer('Номер велосипеда:', reply_markup=None)
        await state.set_state(Form.b_id)
# @questionnaire_router.message(F.text, Form.b_model)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     print(f"=======================")
#     print(message.text)
#
#     await state.set_state(Form.b_id)d
@questionnaire_router.message(F.text,Form.b_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('номер велика')
    if not id_validate(message.text):
        await message.reply("Некоректный номер велика. Попробуйте еще раз")
        return
    await state.update_data(b_id=message.text, user_id=message.from_user.id)
    if dict(await state.get_data())['m_or_e'] != 'Механика':
        iots = await get_pred_iot(await state.get_data())
        if iots:
            await message.answer('Введите номер IoT модуля:', reply_markup=iots_pred(iots))
        else:
            await message.answer('Введите номер IoT модуля:', reply_markup=None)

        await state.set_state(Form.iot_id)
    else:
        await init_work(state,message)
@questionnaire_router.message(F.text,Form.iot_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("номер иот")
    if '|' in message.text:
        iot_number = message.text.split('|')[1]
    else:
        iot_number = message.text
    if not iot_validate(iot_number):
        await message.reply("Некоректный номер IoT. Попробуйте еще раз")
        return
    await state.update_data(iot_id=iot_number, user_id=message.from_user.id)
    await init_work(state,message)
@questionnaire_router.message(F.text == "✏️Изменить ремонт")
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('измененеие ремонта [[[')
    await message.reply("Что делаем?:", reply_markup=edit_work())
    if 'm_or_e' in dict(await state.get_data()):
        await state.set_state(Form.remont_edit)
    else:
        await state.set_state(Form.akb_remont_edit)
@questionnaire_router.message(F.text == "🔄 Отредактировать ремонт")
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print('измененеие ремонта уже записанного')
    await message.reply("Перешли ремонт который будем менять", reply_markup=cancel())
    await state.set_state(Form.saved_remont_edit)
@questionnaire_router.message(F.text,Form.saved_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    if message.text == '❌ Отмена':
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),
                                   caption='Привет я твой помощник по занесению ремонтов. Что будем делать? /start',
                                   reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)
    name,date = message.text.split('\n')[0].split(' | ')
    name = name.split(': ')[1]
    print(await get_user_name(message.from_user.id),name)
    print(message)
    if await get_user_name(message.from_user.id)!=name:
        await message.reply("Это не твой ремонт, ты не можешь его поменять", reply_markup=main_kb(message.from_user.id))
        await state.set_state(Form.client_start)
        return

    if 'Номер велосипеда' in message.text:
        a = await find_remont(name,date,'велик')
    else:
        a = await find_remont(name, date, 'акб')
    await state.clear()
    a['_id'] = str(a['_id'])
    await state.update_data(dict(a))
    await state.update_data(editing_saved=True, user_id=message.from_user.id)
    await state.update_data(message_id =message.message_id, user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    # await state.update_data(norm_time=[], user_id=message.from_user.id)
    if 'Номер велосипеда' in message.text:
        await state.set_state(Form.next_menu)
    else:
        await state.set_state(Form.akb_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())
@questionnaire_router.message(F.text.contains("Запчасти не использовались"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"======================={message.text}")
    print("ЗАпвчасти не использовались")
    data = await state.get_data()
    if 'akb' in data:
        print('акб')
        await state.set_state(Form.akb_menu)
    else:
        await state.set_state(Form.next_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())

