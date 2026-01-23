from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import (works_edit_kb, add_spares, spares_list_for_work, return_spares_group, return_spares,
                              deleting_spares, return_akb_works_kb, deleting_works)
from aiogram.fsm.context import FSMContext
from utils.info import info
from utils.dataframes import df, df_spares
from create_bot import Form
from validators.validators import act_validate, akb_id_validate, capacity_validate
from aiogram.types import ReplyKeyboardRemove
from datetime import timedelta
from db_handler.db_class import get_user_name

# Импортируем тексты и кнопки
from texts import *
from buttons import *

async def init_akb_work(state, message):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    await state.update_data(akb=True, user_id=message.from_user.id)
    await state.update_data(employer_id=message.from_user.id, user_id=message.from_user.id)
    await state.update_data(employer_name=await get_user_name(message.from_user.id), user_id=message.from_user.id)
    await message.answer(await info(state), reply_markup=works_edit_kb(True))
    await state.set_state(Form.akb_menu)

akb_router = Router()

@akb_router.message(F.text, Form.act_akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if not act_validate(message.text):
        await message.reply(TEXT_INVALID_ACT_NUMBER)
        return
    await state.update_data(act_akb_id=message.text, user_id=message.from_user.id)
    await message.answer(TEXT_ENTER_AKB_NUMBER, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.akb_id)

@akb_router.message(F.text, Form.akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if not akb_id_validate(message.text):
        await message.reply(TEXT_INVALID_AKB_NUMBER)
        return
    await state.update_data(akb_id=message.text, user_id=message.from_user.id)
    await state.update_data(start_time=(message.date + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(employer=message.from_user.full_name)
    await init_akb_work(state, message)

@akb_router.message(F.text == BUTTON_ADD_SPARE, Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await state.set_state(Form.getting_akb_spare)
    await message.answer(TEXT_ENTER_SPARE, reply_markup=spares_list_for_work())

@akb_router.message(F.text == BUTTON_ADD_WORK, Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await state.set_state(Form.find_akb_work)
    await message.reply(TEXT_CHOOSE_WORK_TYPE, reply_markup=return_akb_works_kb(await state.get_data(), df))
    await state.set_state(Form.add_akb_work)

@akb_router.message(F.text, Form.add_akb_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text in df.loc[(df['type'] == "АКБ")]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(float(df.loc[(df['works'] == message.text)]['time'].iloc[0]))
        await state.update_data(data=data)
        await state.set_state(Form.getting_akb_spare)
        await message.answer(TEXT_ENTER_SPARE_TYPE, reply_markup=spares_list_for_work())
    else:
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)

@akb_router.message(F.text, Form.getting_akb_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    v_spares = df[df['type'] == 'АКБ'].spares.unique()
    if 'б/у' in message.text:
        await state.update_data(last_spare_type=USED_SPARE_MARK)
    elif message.text == BUTTON_ADD_SPARE:
        await state.update_data(last_spare_type='')
    else:
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return
    await message.reply(TEXT_SPARES_LIST, reply_markup=add_spares(v_spares))
    await state.update_data(spares_variant=list(v_spares))
    await state.set_state(Form.add_akb_spare_)

@akb_router.message(F.text, Form.add_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text in df.loc[(df['type'] == "АКБ")]['spares'].unique():
        if data['last_spare_type'] == '':
            data['spares'].append(message.text)
        else:
            data['spares'].append(message.text + ' ' + data['last_spare_type'])
        await state.update_data(data=data)
        await message.answer(await info(state), reply_markup=works_edit_kb())
    else:
        await message.answer(TEXT_ENTER_SPARE, reply_markup=spares_list_for_work())
    await state.set_state(Form.akb_menu)

@akb_router.message(F.text == BUTTON_DELETE_WORK, Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
    if len(data['works']):
        await message.reply(TEXT_WHAT_TO_DELETE, reply_markup=deleting_works(await state.get_data()))
        await state.set_state(Form.deleting_work)
    else:
        await message.answer(TEXT_NO_WORKS)
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@akb_router.message(F.text == BUTTON_DELETE_SPARE, Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if len(data['spares']):
        await message.reply(TEXT_WHAT_TO_DELETE, reply_markup=deleting_spares(await state.get_data()))
        await state.set_state(Form.akb_deleting_spares)
    else:
        await message.answer(TEXT_NO_SPARES)
        await state.set_state(Form.akb_remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@akb_router.message(F.text, Form.akb_deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========2={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if '| ' in message.text and message.text.split('| ')[1] in data['spares']:
        print(int(message.text.split('| ')[0]))
        data['spares'].pop(int(message.text.split('| ')[0]) - 1)
        await state.update_data(data=data)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
    else:
        await message.answer(TEXT_NO_SUCH_SPARE)
        await state.set_state(Form.akb_remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@akb_router.message(F.text, Form.getting_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    v_spares = df[df['type'] == 'АКБ'].spares.unique()
    if message.text == BUTTON_CANCEL:
        await message.reply(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
        return
    elif 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('Новый')
    await message.reply(TEXT_SPARES_LIST, reply_markup=add_spares(v_spares))
    await state.update_data(spares_variant=v_spares)
    await state.set_state(Form.add_akb_spare_)

@akb_router.message(F.text, Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.client_start)
        await message.answer(TEXT_GO_BACK, reply_markup=works_edit_kb())
        return
    if message.text in df_spares[df_spares['type'] == data['m_or_e']].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply(TEXT_CHOOSE_SPARE, reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.reply(TEXT_CHOOSE_SPARE_GROUP,
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)

@akb_router.message(F.text == BUTTON_ADD_CAPACITY, Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await message.answer(TEXT_ENTER_CAPACITY, reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.get_capacity)

@akb_router.message(F.text, Form.get_capacity)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if capacity_validate(message.text):
        await state.update_data(capacity=message.text)
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb(True))
    else:
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb(True))