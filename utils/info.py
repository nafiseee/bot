client_work_keys = ['work_type', 'full_name', 'phone_number', 'act_id', 'b_model', 'b_id', 'iot_id','act_akb_id','akb_id','capacity']
client_work = ['', '', 'Номер телефона: ', 'Акт №', 'Модель велосипеда: ', 'Номер велосипеда: ', 'IoT: ','Акт №:','Акб №:','Емкость:']
from db_handler.db_class import get_users_colors
# async def info(state):
#     data = await state.get_data()
#     s = f"<b>Мастер:</b> {data['employer_name']} | {data['start_time']}\n\n"
#     for q,w in enumerate(client_work_keys):
#         if w in data:
#             if client_work[q]:
#                 s+=f"<b>{client_work[q]}</b> {data[w]}\n"
#             else:
#                 s+=f"<b>{data[w]}\n</b>"
#     s+='\n<b>Выполненные работы:</b>\n'
#     if data['works']==[]:
#         for i in range(3):
#             s+='____________\n'
#     else:
#         n = 1
#         for i in data['works']:
#             if i not in data['works_count']:
#                 if n<10:
#                     s+=" "
#                 s+=f"   {n}| {i}\n"
#             else:
#                 if data['works_count'][i]==1:
#                     s +=f"{i}\n"
#                 else:
#                     s += f"   {i} ({data['works_count'][i]}x)\n"
#             n+=1
#     s+="\n<b>Запчасти:</b>\n"
#     if data['spares']==[]:
#         for i in range(3):
#             s+='____________\n'
#         else:
#             for i in data['spares']:
#                 if i not in data['works_count']:
#                     s += f"{i}\n"
#                 else:
#                     if data['works_count'][i] == 1:
#                         s +=f"{i}\n"
#                     else:
#                         s +=f"    {i} ({data['works_count'][i]}x)\n"
#     else:
#         print(data['spares_types'])
#         for i in range(len(data['spares'])):
#             if i+1<10:
#                 s+=" "
#             s += f"    {i + 1}| {data['spares'][i]}\n"
#             print(data['spares_types'])
#     s+=f"\n<b>Норма часы:</b> {round(sum(data['norm_time']),1)}👺"
akb_keys = ['act_akb_id','akb_id','capacity']


async def info(state):
    colors = await get_users_colors()
    a = {}
    for i in colors:
        if 'color' in i:
            a[i['tg_id']] = i['color']

    data = await state.get_data()
    s = f"<b>Мастер:</b> {data['employer_name']} | {data['start_time']}\n\n"
    if data['user_id'] in a:
        s+=a[data['user_id']]*10+"\n"
    for index, work_key in enumerate(client_work_keys):
        if work_key in data:
            work_label = client_work[index]
            if work_label:
                s += f"<b>{work_label}</b> {data[work_key]}\n"
            else:
                s += f"<b>{data[work_key]}</b>\n"
    s += '\n<b>Выполненные работы:</b>\n'
    if not data['works']:
        for _ in range(3):
            s += '    ― ― ― ― ― ― ―\n'
    else:
        for number, work in enumerate(data['works'], 1):
            number_str = f" {number}" if number < 10 else str(number)

            if work not in data.get('works_count', {}):
                s += f"   {number_str}| {work}\n"
            else:
                count = data['works_count'][work]
                if count == 1:
                    s += f"{work}\n"
                else:
                    s += f"   {work} ({count}x)\n"
    s += "\n<b>Запчасти:</b>\n"
    if not data['spares']:
        for _ in range(3):
            s += '    ― ― ― ― ― ― ―\n'
    else:
        for i, spare in enumerate(data['spares'], 1):
            number_str = f" {i}" if i < 10 else str(i)
            s += f"   {number_str}| {spare}\n"
        if 'spares_types' in data:
            print("Типы запчастей:", data['spares_types'])
    s += f"\n<b>Норма часы:</b> {round(sum(data['norm_time']), 1)}👺"
    return s
async def info_all_times(a):
    s = "<b>Норма часы за [просто весь период пусть будет]:</b>\n"
    for i in a:
        s+=f"{i}: {a[i]}\n"
    print(s)
    return s