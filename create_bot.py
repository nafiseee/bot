import logging
import os
from aiogram import Bot, Dispatcher,types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.fsm.state import State, StatesGroup
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage
import sys

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import timedelta, datetime
# ... остальные ваши импорты ...

# --- НАСТРОЙКА ЕДИНОГО ЛОГГЕРА ---
log_path = os.path.abspath("bot_debug.log")

# Создаем один логгер для всего проекта
logger = logging.getLogger("BOT_APP")
logger.setLevel(logging.INFO)

# Настраиваем формат
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

# Хендлер для файла (с ротацией, чтобы не забил диск за 3 дня)
file_handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Хендлер для консоли
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("--- ЛОГГЕР ЗАПУЩЕН. ЗАПИСЬ В ФАЙЛ: " + log_path + " ---")
file_handler.flush() # Принудительно выталкиваем данные из буфера в файл

class Form(StatesGroup):
    get_name_employer = State()
    client_start = State()
    full_name = State()
    phone_number = State()
    act_id = State()
    b_or_e = State()
    b_model = State()
    b_id = State()
    iot_id = State()
    find_works = State()
    find_work = State()
    add_work = State()
    find_spare = State()
    find_spare_ = State()
    add_spare = State()
    add_spare_ = State()
    find_spares = State()
    wait = State()
    getting_spare = State()
    getting_spare_ = State()
    remont_edit = State()
    deleting_spares = State()
    next_menu = State()
    akb_menu = State()
    akb_start = State()
    deleting_work = State()
    getting_akb_spare = State()
    getting_akb_spare_ = State()
    set_akb_work = State()
    find_akb_work = State()
    add_akb_work = State()
    act_akb_id = State()
    akb_id = State()
    add_akb_spare = State() #тута
    find_akb_spare = State()
    add_akb_spare_ = State()
    admin = State()
    saved_remont_edit = State()
    akb_remont_edit = State()
    akb_deleting_spares = State()
    get_capacity = State()
    getting_spare_for_work = State()
    norm_times_menu = State()
    norm_times_menu_admin = State()
    get_norm_diapazon = State()
    get_norm_diapazon_admin = State()
    set_spare_count = State()



scheduler = AsyncIOScheduler()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
# def get_connection():
#     try:
#         client = AsyncIOMotorClient('mongodb://localhost:27017/')
#         await client.admin.command('ping')
#         print("✅ MongoDB подключена успешно")
#         return  client
#     except Exception as e:
#         print(f"❌ Ошибка подключения по localhost: {e}")
#         try:
#
#             client = AsyncIOMotorClient('mongodb://adminuser:adminpassword@mongodb:27017/')
#             await client.admin.command('ping')
#             print("✅ MongoDB подключена успешно по ip")
#             return client
#         except Exception as e:
#             print(f"❌ Ошибка подключения: {e}")
#             return False

async_client = AsyncIOMotorClient('mongodb://adminuser:adminpassword@mongodb:27017/') #server
#async_client = AsyncIOMotorClient('mongodb://localhost:27017/') #local
print('подключение к монго')
async_db = async_client.telegram_bot
electro = async_db.electro
mechanical = async_db.mechanical
akb = async_db.akb
users = async_db.users
messages = async_db.messages
new_works = async_db.new_works


print(config('REDIS_USER'))
print(os.getenv('REDIS_PASSWORD'))
# redis = Redis(
#     host='redis',  # имя контейнера Redis
#     port=6379,
#     socket_connect_timeout=10# ← Берем из окружения
# )

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
from datetime import timedelta
dp = Dispatcher(storage=RedisStorage.from_url("redis://redis:6379/0",state_ttl=timedelta(hours=24),data_ttl=timedelta(hours=24) )) # server

#dp = Dispatcher(storage=RedisStorage.from_url("redis://127.0.0.1:6379/0",state_ttl=timedelta(hours=24),data_ttl=timedelta(hours=24) )) #local

from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable


class FSMTracingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        state = data.get("state")
        user = data.get("event_from_user")
        user_id = user.id if user else "Unknown"

        event_content = "N/A"
        if event.message:
            event_content = f"Msg: {event.message.text}"
        elif event.callback_query:
            event_content = f"Cb: {event.callback_query.data}"

        state_before = await state.get_state() if state else "No State"

        # Используем наш единый logger
        logger.info(f"FSM_CHECK: User {user_id} | Input: {event_content} | State BEFORE: {state_before}")

        try:
            result = await handler(event, data)
        except Exception as e:
            logger.error(f"FSM_ERROR: User {user_id} crashed handler! Error: {e}", exc_info=True)
            file_handler.flush()  # Сразу пишем ошибку на диск
            raise e

        state_after = await state.get_state() if state else "No State"

        if state_before != state_after:
            logger.info(f"FSM_CHANGE: User {user_id} | {state_before} -> {state_after}")

        # ПРИНУДИТЕЛЬНО СБРАСЫВАЕМ НА ДИСК
        file_handler.flush()

        return result


# Регистрация в диспетчере (сделайте это первой среди мидлварей)
dp.update.outer_middleware(FSMTracingMiddleware())
print('подключение к редис')
