from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import works_edit_kb,works_groups,return_works_kb,spares_list_for_work,deleting_works
from aiogram.fsm.context import FSMContext
from utils.info import info
from utils.dataframes import df
from create_bot import Form

works_router = Router()

@works_router.message(F.text == "➕ Добавить работу",Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()}\n=============================")
    print("Добавление работы")
    await state.set_state(Form.find_work)
    await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(), df))
    await state.set_state(Form.find_work)
@works_router.message(F.text=="🗑 Удалить работу",Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()}\n=============================")
    print("Удалить работу")
    data = await state.get_data()
    if message.text == '❌ Отмена':
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
    if len(data['works']):
        await message.reply("Что удалить?", reply_markup=deleting_works(await state.get_data()))
        await state.set_state(Form.deleting_work)
    else:
        await message.answer('Работ и так нет.')
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
@works_router.message(F.text,Form.deleting_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()}\n=============================")
    print("Удаление ремонта")
    data = await state.get_data()
    if '| 'in message.text and  message.text.split('| ')[1] in  data['works']:
        data['works'].remove(message.text.split('| ')[1])
        await message.answer(f"Удалено: {message.text.split('| ')[1]}", reply_markup=works_edit_kb())
        data['norm_time'].pop(int(message.text.split('| ')[0])-1)
        await state.update_data(works = data['works'])
        await state.update_data(norm_time=data['norm_time'])
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    elif message.text == "❌ Отмена":
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
    else:
        await message.answer('Нет такой работы')
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
@works_router.message(F.text,Form.find_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()}\n=============================")
    print("поиск работы")
    if message.text=='❌ Отмена':
        await state.set_state(Form.next_menu)
        await message.answer('Что делаем?',reply_markup=works_edit_kb())
        return
    if message.text in df[df['type']==dict(await state.get_data())['m_or_e']].group.unique():
        await state.update_data(last_group=message.text)
        await state.set_state(Form.add_work)
        await message.reply("Выбери работу:",reply_markup=return_works_kb(await state.get_data(),df))
    else:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(),df))
        await state.set_state(Form.find_work)
#ДОБАВЛЕНИЕ РАБОТЫ
@works_router.message(F.text,Form.add_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()}\n=============================")
    print("добавление работы")
    data = await state.get_data()
    if 'Отмена' in message.text:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(), df))
        await state.set_state(Form.find_work)
        return
    if message.text in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(float(
            df.loc[((df['group']==data['last_group'])&
                    (df['type']==data['m_or_e'])&
                    (df['works']==message.text))]['time'].iloc[0]))
        await state.update_data(data=data)
        await state.set_state(Form.getting_spare_for_work)
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
    else:
        await message.reply("Выбери работу:", reply_markup=return_works_kb(await state.get_data(),df))
        await state.set_state(Form.add_work)

