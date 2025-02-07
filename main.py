import asyncio, sqlalchemy
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import app.handlers
from database import models
import logging, sys, datetime
from confidential import token, admin_id

logger = logging.getLogger(__name__)
log_file = 'logs.txt'


def log_file_printer(printing, log_file_):
    file = open(log_file_, "a", encoding='utf-8')
    logger.info(printing)
    file.write(str(datetime.datetime.now()) + ' :' + str(printing) + '\n')
    file.close()

bot = Bot(token=token)
dp = Dispatcher()
async def main():
    logging.basicConfig(filename='', level=logging.INFO)
    log_file_printer(f"Бот запустился", log_file)
    dp.include_router(app.handlers.router)
    await dp.start_polling(bot)
    log_file_printer(f"Бот остановился", log_file)

if __name__ == '__main__':
    models.execute_query(models.create_connection(models.path), models.create_users_table)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен вручную.')

