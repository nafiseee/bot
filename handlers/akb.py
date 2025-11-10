from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import (works_edit_kb,add_spares,spares_list_for_work,return_spares_group,return_spares,deleting_spares,
                              return_akb_works_kb,deleting_works)
from aiogram.fsm.context import FSMContext
from utils.info import info
from utils.dataframes import df,df_spares
from create_bot import Form
from validators.validators import act_validate,akb_id_validate,capacity_validate
from aiogram.types import ReplyKeyboardRemove
from datetime import timedelta
from db_handler.db_class import get_user_name
async def init_akb_work(state,message):
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
@akb_router.message(F.text,Form.act_akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_akb_id=message.text, user_id=message.from_user.id)
    await message.answer('Номер акб:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.akb_id)
@akb_router.message(F.text,Form.akb_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if not akb_id_validate(message.text):
        await message.reply("Некоректный номер акб. Попробуйте еще раз")
        return
    await state.update_data(akb_id=message.text, user_id=message.from_user.id)
    await state.update_data(start_time=(message.date + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(employer=message.from_user.full_name)
    await init_akb_work(state,message)
@akb_router.message(F.text=='➕ Добавить запчасть',Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await state.set_state(Form.getting_akb_spare)
    await message.answer("Введи зч", reply_markup=spares_list_for_work())
@akb_router.message(F.text == "➕ Добавить работу",Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await state.set_state(Form.find_akb_work)
    await message.reply("Выбери вид работы:", reply_markup=return_akb_works_kb(await state.get_data(), df))
    await state.set_state(Form.add_akb_work)
@akb_router.message(F.text,Form.add_akb_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text in df.loc[(df['type']=="АКБ")]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(float(df.loc[(df['works']==message.text)]['time'].iloc[0]))
        await state.update_data(data=data)
        await state.set_state(Form.getting_akb_spare)
        await message.answer("Введи тип зч", reply_markup=spares_list_for_work())
    else:
        await message.answer(await(info(state)), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
@akb_router.message(F.text,Form.getting_akb_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    v_spares = df[df['type']=='АКБ'].spares.unique()
    if 'б/у' in message.text:
        await state.update_data(last_spare_type = '[б/У]')
    elif message.text == "Добавить запчасть":
        await state.update_data(last_spare_type = '')
    else:
        await state.set_state(Form.akb_menu)
        await message.answer(await(info(state)), reply_markup=works_edit_kb())
        return
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))

    await state.update_data(spares_variant=list(v_spares))
    await state.set_state(Form.add_akb_spare_)
@akb_router.message(F.text,Form.add_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text in df.loc[(df['type']=="АКБ")]['spares'].unique():
        if data['last_spare_type'] == '':
            data['spares'].append(message.text)
        else:
            data['spares'].append(message.text + ' ' + data['last_spare_type'])
        await state.update_data(data=data)
        await message.answer(await(info(state)),reply_markup=works_edit_kb())

    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
    await state.set_state(Form.akb_menu)
@akb_router.message(F.text=="🗑 Удалить работу",Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text == '❌ Отмена':
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
    if len(data['works']):
        await message.reply("Что удалить?", reply_markup=deleting_works(await state.get_data()))
        await state.set_state(Form.deleting_work)
    else:
        await message.answer('Работ и так нет.')
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
@akb_router.message(F.text=="🗑 Удалить запчасть",Form.akb_remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if len(data['spares']):
        await message.reply("Что удалить?", reply_markup=deleting_spares(await state.get_data()))
        await state.set_state(Form.akb_deleting_spares)
    else:
        await message.answer('Запчастей и так нет.')
        await state.set_state(Form.akb_remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())
@akb_router.message(F.text,Form.akb_deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========2={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if '| 'in message.text and  message.text.split('| ')[1] in  data['spares']:
        print(int(message.text.split('| ')[0]))
        data['spares'].pop(int(message.text.split('| ')[0])-1)
        await state.update_data(data = data)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
    else:
        await message.answer('Нет такой запчасти')
        await state.set_state(Form.akb_remont_edit)
        await message.answer(await info(state), reply_markup=works_edit_kb())
@akb_router.message(F.text,Form.getting_akb_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    v_spares = df[df['type'] == 'АКБ'].spares.unique()
    if message.text == "❌ Отмена":
        await message.reply(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.akb_menu)
        return
    elif 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('Новый')
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.update_data(spares_variant=v_spares)
    await state.set_state(Form.add_akb_spare_)


@akb_router.message(F.text,Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    data = await state.get_data()
    if message.text=='❌ Отмена':
        await state.set_state(Form.client_start)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    if message.text in df_spares[df_spares['type']==data['m_or_e']].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply("Выбери запчасть:",reply_markup=return_spares(df_spares,await state.get_data()))
    else:
        await message.reply("Выбери группу запчастей:",
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)
@akb_router.message(F.text=="Добавить емкость 📉",Form.akb_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    await message.answer("Напиши емкость:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.get_capacity)
@akb_router.message(F.text,Form.get_capacity)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    if capacity_validate(message.text):
        await state.update_data(capacity = message.text)
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb(True))
    else:
        await state.set_state(Form.akb_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb(True))



#=======================================================================================================================

# @akb_router.message(F.text,Form.add_akb_spare)
# async def start1_questionnaire_process(message: Message, state: FSMContext):
#     print("добавление запччасти")
#     data = await state.get_data()
#     if message.text in list(data['spares_variant']):
#         data['spares'].append(message.text)
#         await state.update_data(data=data)
#         await message.answer(await info(state), reply_markup=works_edit_kb())
#         await state.set_state(Form.akb_menu)
#     else:
#         await message.answer("Введи зч", reply_markup=spares_list_for_work())
#         await state.set_state(Form.find_spare)