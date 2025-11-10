import asyncio

from create_bot import bot, dp, scheduler
from handlers.start import start,questionnaire_router
from handlers.works import works_router
from handlers.spares import spares_router
from handlers.akb import akb_router
from handlers.other  import other
from handlers.admin_panel import  admin_router



async def main():

    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(works_router)
    dp.include_router(start)
    dp.include_router(other)
    dp.include_router(akb_router)
    dp.include_router(questionnaire_router)
    dp.include_router(spares_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())