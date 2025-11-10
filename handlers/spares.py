from aiogram import Router, F
from aiogram.types import Message
from keyboards.all_kb import works_edit_kb,add_spares,spares_list_for_work,return_spares_group,return_spares,deleting_spares
from aiogram.fsm.context import FSMContext
from utils.info import info
from utils.dataframes import df,df_spares
from create_bot import Form

spares_router = Router()


@spares_router.message(F.text == '➕ Добавить запчасть', Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Добавить зч")
    await state.set_state(Form.getting_spare_)
    await message.answer("Введи зч", reply_markup=spares_list_for_work())


@spares_router.message(F.text == "🗑 Удалить запчасть", Form.remont_edit)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("удалить запчасть")
    data = await state.get_data()
    spares_list = data.get('spares', [])

    if spares_list:
        await message.answer("Что удалить?", reply_markup=deleting_spares(data))
        await state.set_state(Form.deleting_spares)
    else:
        await message.answer('Запчастей и так нет.')
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())


@spares_router.message(F.text, Form.deleting_spares)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("удаление запчастей")
    data = await state.get_data()
    spares_list = data.get('spares', [])

    if message.text == "❌ Отмена":
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return

    # Безопасное удаление по индексу
    if '|' in message.text:
        spare_number = int(message.text.split('|')[0].strip()) - 1
        print(spare_number)
        removed_spare = spares_list.pop(spare_number-1)
        await state.update_data(spares=spares_list)
        print(spares_list)
        await message.answer(f"Удалено: {removed_spare}")
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        return

    await message.answer('Нет такой запчасти')
    await state.set_state(Form.next_menu)
    await message.answer(await info(state), reply_markup=works_edit_kb())


@spares_router.message(F.text.contains("Запчасти не использовались"))
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

    if message.text == "❌ Отмена":
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())

        return
    elif 'б/у' in message.text.lower():
        await state.update_data(last_spare_type='[б/У]')
    else:
        await state.update_data(last_spare_type='')

    # Проверяем наличие необходимых данных
    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer("Ошибка: не определен тип оборудования")
        await state.set_state(Form.next_menu)
        return

    await message.answer("Выбери группу запчастей:", reply_markup=return_spares_group(df_spares, data))
    await state.set_state(Form.find_spare_)


@spares_router.message(F.text, Form.find_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("поиск зч_")
    data = await state.get_data()

    if message.text == '❌ Отмена':
        await state.set_state(Form.next_menu)
        await message.answer('Что делаем?', reply_markup=works_edit_kb())
        return

    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer("Ошибка данных")
        await state.set_state(Form.next_menu)
        return

    if message.text in df_spares[df_spares['type'] == m_or_e].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.answer("Выбери запчасть:", reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.answer("Выбери группу запчастей:",
                             reply_markup=return_spares_group(df_spares, await state.get_data()))


@spares_router.message(F.text, Form.add_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("добавление запчасти_")
    data = await state.get_data()

    # Проверяем необходимые данные
    last_group = data.get('last_spare_group')
    m_or_e = data.get('m_or_e')

    if message.text == '❌ Отмена':
        await state.set_state(Form.next_menu)
        await message.answer('Что делаем?', reply_markup=works_edit_kb())
        return
    if not last_group or not m_or_e:
        await message.answer("Ошибка данных, начните заново")
        await state.set_state(Form.next_menu)
        return

    # Получаем доступные запчасти
    available_spares = df_spares.loc[
        (df_spares['group'] == last_group) &
        (df_spares['type'] == m_or_e)
        ]['spares'].unique()
    print('f',available_spares)
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

        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer("Запчасть не найдена, попробуйте снова",
                             reply_markup=spares_list_for_work())


@spares_router.message(F.text, Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("Поиск запчасти")
    data = await state.get_data()

    if message.text == '❌ Отмена':
        await state.set_state(Form.client_start)
        await message.answer('Что делаем?', reply_markup=works_edit_kb())
        return

    m_or_e = data.get('m_or_e')
    if not m_or_e:
        await message.answer("Ошибка данных")
        await state.set_state(Form.next_menu)
        return

    if message.text in df_spares[df_spares['type'] == m_or_e].group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare)
        await message.answer("Выбери запчасть:", reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.answer("Выбери группу запчастей:",
                             reply_markup=return_spares_group(df_spares, await state.get_data()))


@spares_router.message(F.text, Form.getting_spare_for_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("получение запчасти")
    data = await state.get_data()
    if message.text == '❌ Отмена':  # ДОБАВИТЬ обработку отмены
        await state.set_state(Form.next_menu)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        return

    works_list = data.get('works', [])
    if not works_list:
        await message.answer("Нет работ для добавления запчастей")
        await state.set_state(Form.next_menu)
        return

    last_work = works_list[-1]
    v_spares = df[df['works'] == last_work]['spares'].unique()

    if message.text not in['Добавить запчасть','Добавить б/у запчасть','Запчасти не использовались / Отмена']:
        await state.set_state(Form.getting_spare_for_work)
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
        return

    if 'б/у' in message.text.lower():
        await state.update_data(last_spare_type='[б/У]')
    elif '❌ Отмена' == message.text:
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        return
    else:
        await state.update_data(last_spare_type='')

    await message.answer("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_spare)
    print(v_spares)
    await state.update_data(spares_variant=list(v_spares))



@spares_router.message(F.text, Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(f"========={await state.get_state()} {message.from_user.full_name} {message.text}\n=============================")
    print("добавление запчасти", message.text)
    data = await state.get_data()
    spares_variant = data.get('spares_variant', [])

    if message.text == '❌ Отмена':
        await state.set_state(Form.getting_spare_for_work)
        await message.answer('Выбкри тип запчасти', reply_markup=spares_list_for_work())
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

        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer("Запчасти:", reply_markup=add_spares(spares_variant))
        await state.set_state(Form.add_spare)