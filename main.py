from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config

bot = Bot(token=Config.token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


def main():
    from handlers import dp
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        pass



if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
