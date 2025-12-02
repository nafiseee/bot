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
    add_akb_spare = ()
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

#async_client = AsyncIOMotorClient('mongodb://adminuser:adminpassword@mongodb:27017/') #server
async_client = AsyncIOMotorClient('mongodb://localhost:27017/') #local
print('подключение к монго')
async_db = async_client.telegram_bot
electro = async_db.electro
mechanical = async_db.mechanical
akb = async_db.akb
users = async_db.users
messages = async_db.messages

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
print(config('REDIS_USER'))
print(os.getenv('REDIS_PASSWORD'))
# redis = Redis(
#     host='redis',  # имя контейнера Redis
#     port=6379,
#     socket_connect_timeout=10# ← Берем из окружения
# )

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
from datetime import timedelta
#dp = Dispatcher(storage=RedisStorage.from_url("redis://redis:6379/0",state_ttl=timedelta(hours=24),data_ttl=timedelta(hours=24) )) # server

dp = Dispatcher(storage=RedisStorage.from_url("redis://127.0.0.1:6379/0",state_ttl=timedelta(hours=24),data_ttl=timedelta(hours=24) )) #local
print('подключение к редис')
