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
                         , caption=get_product_by_id(1).name + ' \nВага: ' + str(get_product_by_id(1).weight) +
                                   ' г\nЦіна: ' + str(get_product_by_id(1).price) + ' грн\nОпис: '
                                   + get_product_by_id(1).description, reply_markup=get_keyboard(0))


# endregion

# region text


@dp.message_handler(Text(equals=['Найти музику']), state=None)
async def find_music(message: types.Message):
    await message.answer('Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()

@dp.message_handler(Text(equals=['Вихід']))
async def find_music(message: types.Message):
    await message.answer('Back to MUSIC🎸🎸🎸\nВедіть силку або напишіть назву відео з ютуба:',reply_markup=start_keyboard)
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

@dp.callback_query_handler(kall.filter(action='next'))
async def candy_next(callback: types.CallbackQuery,callback_data: dict):

    amount = int(callback_data['amount'])
    amount += 1
    prod = get_product_by_id(amount)
    if prod is not None:
        await callback.message.edit_media(media=types.InputMediaPhoto(media=open('pictures/' + prod.name + '.jpeg', 'rb'),
                                       caption=prod.name + ' \nВага: ' + str(
                                        prod.weight) +
                                        ' г\nЦіна: ' + str(prod.price) + ' грн\nОпис: '
                                        + prod.description), reply_markup=get_keyboard(amount))
@dp.callback_query_handler(kall.filter(action='back'))
async def candy_back(callback: types.CallbackQuery,callback_data: dict):
    amount = int(callback_data['amount'])
    amount -= 1
    prod = get_product_by_id(amount)
    if prod is not None:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=open('pictures/' + prod.name + '.jpeg', 'rb'),
                                        caption=prod.name + ' \nВага: ' + str(
                                            prod.weight) +
                                                ' г\nЦіна: ' + str(prod.price) + ' грн\nОпис: '
                                                + prod.description), reply_markup=get_keyboard(amount))
# endregion
