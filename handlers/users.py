from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from keyboards import *
from main import bot, dp
from misc import DownloadMusic
from states import UserStates
from database import *


# region commands
@dp.message_handler(Command('start'))
async def start_cmd(message: types.Message):
    await bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}', reply_markup=start_keyboard)


@dp.message_handler(Command('candy'))
async def candy_cmd(message: types.Message):
    await message.reply(text='CANDYYYYYYYYYYYYYYYYYYYYYYY🍫🍭🍬🍭🍩', reply_markup=candy_menu_keyboard)
    await bot.send_photo(message.chat.id, photo=open('pictures/' + get_product_by_id(1).name + '.jpeg', 'rb')
                         , caption=get_product_by_id(1).name + '\nВага: ' + str(get_product_by_id(1).weight) +
                                   ' г\nЦіна: ' + str(get_product_by_id(1).price) + ' грн\nОпис: '
                                   + get_product_by_id(1).description , reply_markup=shop_keyboard)



# endregion

# region text


@dp.message_handler(Text(equals=['Найти музику']), state=None)
async def find_music(message: types.Message):
    await message.answer('Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()


@dp.message_handler(state=UserStates.state)
async def find_music(message: types.Message, state: FSMContext):
    await state.finish()
    down = DownloadMusic(message)
    await down.download()


# endregion

# region callbacks


@dp.callback_query_handler(text='continue')
async def continue_music(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()
# endregion
