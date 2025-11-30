import re
from utils.dataframes import df
def name_validate(text):
    pattern = r'^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$'
    return bool(re.match(pattern, text))
def phone_validate(text):
    pattern = r'^(\+7|8)\d{10}$'
    return bool(re.match(pattern, text))
def act_validate(text):
    pattern = r'[0-9]+$'
    return bool(re.match(pattern, text)) or text == 'Акт отсутствует'
def capacity_validate(text):
    pattern = r'^[0-9]*\.?[0-9]+$'
    return bool(re.match(pattern, text))
def model_validate(text):
    return text in ["Шаркусь монстр 15","Шаркусь монстр 20","Мингто монстр 20","Монстр про","Крути 15",
                    "Kruti 29","Kruti 27.5","Forward 29","Forward 27.5,"
                    "Желтый","Лонг"]
def id_validate(text):
    return act_validate(text)
def iot_validate(text):
    return act_validate(text)
def bycycle_type_validate(text):
    return text in ['🔩 Механика','⚡ Электро']
def work_is_true(text):
    return text in df['works']
def akb_id_validate(text):
    return act_validate(text)
