from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import works_edit_kb, add_spares, spares_list_for_work, return_spares_group, return_spares, deleting_spares, spare_count_kb
from aiogram.fsm.context import FSMContext
from utils.info import info
from utils.dataframes import df, df_spares
from create_bot import Form

# Импортируем тексты и кнопки
from texts import *
from buttons import *

spares_router = Router()

@spares_router.message(F.text == BUTTON_ADD_SPARE, Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Добавить зч")
    await state.set_state(Form.getting_spare_)
    await message.answer(TEXT_ENTER_SPARE, reply_markup=spares_list_for_work())

@spares_router.message(F.text == BUTTON_DELETE_SPARE, Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("удалить запчасть")
    data = await state.get_data()
    spares_list = data.get('spares', [])

    if spares_list:
        await message.answer(TEXT_WHAT_TO_DELETE, reply_markup=deleting_spares(data))
        await state.set_state(Form.deleting_spares)
    else:
        await message.answer(TEXT_NO_SPARES)
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())

@spares_router.message(F.text, Form.deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("удаление запчастей")
    data = await state.get_data()
    spares_list = data.get('spares', [])

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return

    # Безопасное удаление по индексу
    if '|' in message.text:
        spare_number = int(message.text.split('|')[0].strip())
        print(spare_number)
        removed_spare = spares_list.pop(spare_number - 1)
        await state.update_data(spares=spares_list)
        print(spares_list)
        await message.answer(f"{TEXT_DELETED}: {removed_spare}")
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        return

    await message.answer(TEXT_NO_SUCH_SPARE)
    await state.set_state(Form.next_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())

@spares_router.message(F.text.contains(TEXT_NO_SPARES_USED))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Запчасти не использовались")
    await state.set_state(Form.next_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())

@spares_router.message(F.text, Form.getting_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Получение запчастей_")
    data = await state.get_data()

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return
    elif 'б/у' in message.text.lower():
        await state.update_data(last_spare_type=USED_SPARE_MARK)
    else:
        await state.update_data(last_spare_type='')

    # Проверяем наличие необходимых данных
    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer(TEXT_ERROR_EQUIPMENT_TYPE)
        await state.set_state(Form.next_menu)
        return

    await message.answer(TEXT_CHOOSE_SPARE_GROUP, reply_markup=return_spares_group(df_spares, data))
    await state.set_state(Form.find_spare_)

@spares_router.message(F.text, Form.find_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("поиск зч_")
    data = await state.get_data()

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.next_menu)
        await message.answer(TEXT_WHAT_TO_DO, reply_markup=works_edit_kb())
        return

    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer(TEXT_DATA_ERROR)
        await state.set_state(Form.next_menu)
        return

    if message.text in df_spares[df_spares['type'] == m_or_e].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.answer(TEXT_CHOOSE_SPARE, reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.answer(TEXT_CHOOSE_SPARE_GROUP,
                             reply_markup=return_spares_group(df_spares, await state.get_data()))

@spares_router.message(F.text, Form.add_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("добавление запчасти_")
    data = await state.get_data()

    # Проверяем необходимые данные
    last_group = data.get('last_spare_group')
    m_or_e = data.get('m_or_e')

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.next_menu)
        await message.answer(TEXT_WHAT_TO_DO, reply_markup=works_edit_kb())
        return
    if not last_group or not m_or_e:
        await message.answer(TEXT_DATA_ERROR_RESTART)
        await state.set_state(Form.next_menu)
        return

    # Получаем доступные запчасти
    available_spares = df_spares.loc[
        (df_spares['group'] == last_group) &
        (df_spares['type'] == m_or_e)
        ]['spares'].unique()
    print('f', available_spares)
    if message.text in available_spares:
        # Формируем запчасть с учетом типа
        spare_to_add = message.text
        spare_type = data.get('last_spare_type', '')
        if spare_type:
            spare_to_add += ' ' + spare_type

        # Безопасно обновляем список запчастей
        current_spares = data.get('spares', [])
        current_spares.append(spare_to_add)
        await state.update_data(spares=current_spares)

        await state.set_state(Form.set_spare_count)
        await message.answer(TEXT_ENTER_QUANTITY, reply_markup=spare_count_kb())
    else:
        await message.answer(TEXT_SPARE_NOT_FOUND,
                             reply_markup=spares_list_for_work())

@spares_router.message(F.text, Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Поиск запчасти")
    data = await state.get_data()

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.client_start)
        await message.answer(TEXT_WHAT_TO_DO, reply_markup=works_edit_kb())
        return

    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer(TEXT_DATA_ERROR)
        await state.set_state(Form.next_menu)
        return

    if message.text in df_spares[df_spares['type'] == m_or_e].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare)
        await message.answer(TEXT_CHOOSE_SPARE, reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.answer(TEXT_CHOOSE_SPARE_GROUP,
                             reply_markup=return_spares_group(df_spares, await state.get_data()))

@spares_router.message(F.text, Form.getting_spare_for_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("получение запчасти")
    data = await state.get_data()
    if message.text == BUTTON_CANCEL:  # ДОБАВИТЬ обработку отмены
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return

    works_list = data.get('works', [])
    if not works_list:
        await message.answer(TEXT_NO_WORKS_FOR_SPARES)
        await state.set_state(Form.next_menu)
        return

    last_work = works_list[-1]
    v_spares = df[df['works'] == last_work]['spares'].unique()

    if message.text not in [BUTTON_ADD_SPARE, BUTTON_ADD_USED_SPARE, TEXT_NO_SPARES_CANCEL]:
        await state.set_state(Form.getting_spare_for_work)
        await message.answer(TEXT_ENTER_SPARE, reply_markup=spares_list_for_work())
        return

    if 'б/у' in message.text.lower():
        await state.update_data(last_spare_type=USED_SPARE_MARK)
    elif BUTTON_CANCEL == message.text:
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        return
    else:
        await state.update_data(last_spare_type='')

    await message.answer(TEXT_SPARES_LIST, reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_spare)
    print(v_spares)
    await state.update_data(spares_variant=list(v_spares))

@spares_router.message(F.text, Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("добавление запчасти", message.text)
    data = await state.get_data()
    spares_variant = data.get('spares_variant', [])

    if message.text == BUTTON_CANCEL:
        await state.set_state(Form.getting_spare_for_work)
        await message.answer(TEXT_CHOOSE_SPARE_TYPE, reply_markup=spares_list_for_work())
        return
    print(list(spares_variant))
    if message.text in list(spares_variant):
        # Формируем запчасть с учетом типа
        spare_to_add = message.text
        spare_type = data.get('last_spare_type', '')
        if spare_type:
            spare_to_add += ' ' + spare_type

        # Безопасно обновляем список запчастей
        current_spares = data.get('spares', [])
        current_spares.append(spare_to_add)
        await state.update_data(spares=current_spares)
        await state.set_state(Form.set_spare_count)
        await message.answer(TEXT_ENTER_QUANTITY, reply_markup=spare_count_kb())
    else:
        await message.answer(TEXT_SPARES_LIST, reply_markup=add_spares(spares_variant))
        await state.set_state(Form.add_spare)

@spares_router.message(F.text, Form.set_spare_count)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if message.text in ['1', '2']:
        if message.text == '2':
            data = await state.get_data()
            current_spares = data.get('spares', [])
            current_spares.append(current_spares[-1])
            await state.update_data(spares=current_spares)
            await message.answer(await info(state), reply_markup=works_edit_kb())
            await state.set_state(Form.next_menu)
        else:
            await message.answer(await info(state), reply_markup=works_edit_kb())
            await state.set_state(Form.next_menu)
    else:
        await state.set_state(Form.set_spare_count)
        await message.answer(TEXT_ENTER_QUANTITY, reply_markup=spare_count_kb())
    print(await state.get_data())

