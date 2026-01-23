from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Импортируем кнопки
from buttons import *

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text=BUTTON_CLIENT_REPAIR), KeyboardButton(text=BUTTON_TECH_SERVICE)],
        [KeyboardButton(text=BUTTON_BATTERY), KeyboardButton(text="☠️☠️☠️☠️")],
        [KeyboardButton(text=BUTTON_NORM_HOURS_USER)],
        [KeyboardButton(text=BUTTON_EDIT_SAVED_REPAIR)]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=BUTTON_ADMIN_PANEL)])
    if user_telegram_id in [168604695, 1003927607, 933028899]:
        kb_list.append([KeyboardButton(text=BUTTON_MUSIC)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def m_or_e_kb():
    kb_list = [
        [KeyboardButton(text="🔩 Механика")],
        [KeyboardButton(text="⚡ Электро")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def akt_zero():
    kb_list = [
        [KeyboardButton(text="Акт отсутствует")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def works_edit_kb(akb=False):
    if akb:
        kb_list = [
            [KeyboardButton(text=BUTTON_ADD_WORK), KeyboardButton(text=BUTTON_ADD_SPARE)],
            [KeyboardButton(text=BUTTON_EDIT_REPAIR)],
            [KeyboardButton(text=BUTTON_ADD_CAPACITY)],
            [KeyboardButton(text=BUTTON_SAVE_REPAIR)],
            [KeyboardButton(text=BUTTON_CANCEL_REPAIR)]
        ]
    else:
        kb_list = [
            [KeyboardButton(text=BUTTON_ADD_WORK), KeyboardButton(text=BUTTON_ADD_SPARE)],
            [KeyboardButton(text=BUTTON_EDIT_REPAIR)],
            [KeyboardButton(text=BUTTON_SAVE_REPAIR)],
            [KeyboardButton(text=BUTTON_CANCEL_REPAIR)]
        ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def akb_menu():
    kb_list = [
        [KeyboardButton(text=BUTTON_ADD_WORK), KeyboardButton(text=BUTTON_ADD_SPARE)],
        [KeyboardButton(text=BUTTON_SAVE_REPAIR)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def akb_works(df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type'] == "АКБ"].works.unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def akb_spares(df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type'] == "АКБ"].spares.unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def akb_start_kb():
    kb_list = [
        [KeyboardButton(text="Начать работу")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def b_models(a):
    print(a)
    kb_list = [
        [KeyboardButton(text="Шаркусь монстр 15")],
        [KeyboardButton(text="Шаркусь монстр 20")],
        [KeyboardButton(text="Мингто монстр 20")],
        [KeyboardButton(text="Монстр про")],
        [KeyboardButton(text="Крути 15")],
        [KeyboardButton(text="Желтый")],
        [KeyboardButton(text="Лонг")],
    ]
    kb_list2 = [
        [KeyboardButton(text="Forward 27.5")],
        [KeyboardButton(text="Forward 29")],
        [KeyboardButton(text="Kruti 27.5")],
        [KeyboardButton(text="Kruti 29")]
    ]
    if a == 'Механика':
        return ReplyKeyboardMarkup(
            keyboard=kb_list2,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )

def works_groups(data, df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type'] == data['m_or_e']]['group'].unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def add_spares(a):
    kb_list = [[KeyboardButton(text=i)] for i in a]
    kb_list.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def spares_list_for_work():
    kb_list = [
        [KeyboardButton(text=BUTTON_ADD_SPARE)],
        [KeyboardButton(text=BUTTON_ADD_USED_SPARE)],
        [KeyboardButton(text=TEXT_NO_SPARES_CANCEL)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def return_works_kb(data, df):
    kb = [[KeyboardButton(text=i)] for i in df.loc[((df['group'] == data['last_group']) & (df['type'] == data['m_or_e']))]['works'].unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    for i in kb:
        print(i)
    return keyboard

def return_akb_works_kb(data, df):
    kb = [[KeyboardButton(text=i)] for i in df.loc[(df['type'] == "АКБ")]['works'].unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    for i in kb:
        print(i)
    return keyboard

def return_spares_group(df, data):
    kb = [[KeyboardButton(text=i)] for i in df[df['type'] == data['m_or_e']].group.unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def return_spares(df, data):
    print(data)
    kb = [[KeyboardButton(text=i)] for i in df.loc[((df['group'] == data['last_spare_group']) & (df['type'] == data['m_or_e']))]['spares'].unique()]
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def edit_work():
    kb_list = [
        [KeyboardButton(text=BUTTON_DELETE_WORK)],
        [KeyboardButton(text=BUTTON_DELETE_SPARE)],
        [KeyboardButton(text=BUTTON_CANCEL)],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def iots_pred(iots):
    kb = [[KeyboardButton(text=i)] for i in iots]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def deleting_works(data):
    print(data)
    kb = []
    for q in range(len(data['works'])):
        kb.append([KeyboardButton(text=f"{str(q + 1)}| {data['works'][q]}")])
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    print(data['works'])
    return keyboard

def deleting_spares(data):
    print(data)
    kb = []
    for q in range(len(data['spares'])):
        kb.append([KeyboardButton(text=f"{str(q + 1)}| {data['spares'][q]}")])
    kb.append([KeyboardButton(text=BUTTON_CANCEL)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    print(data['works'])
    return keyboard

def to_delete_work(data, df):
    kb = [[KeyboardButton(text=i)] for i in data['works']]
    kb.append([KeyboardButton(text=BUTTON_CANCEL_SHORT)])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    for i in kb:
        print(i)
    return keyboard

def admin_buttons():
    kb_list = [
        [KeyboardButton(text=BUTTON_NORM_HOURS_ALL)],
        [KeyboardButton(text=BUTTON_USED_SPARES)],
        [KeyboardButton(text=BUTTON_ALL_WORKS)],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def cancel():
    kb_list = [[KeyboardButton(text=BUTTON_CANCEL)]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def norm_times_menu():
    kb_list = [
        [KeyboardButton(text=BUTTON_SELECT_RANGE)],
        [KeyboardButton(text=BUTTON_CANCEL)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def spare_count_kb():
    kb_list = [
        [KeyboardButton(text="1"), KeyboardButton(text="2")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard