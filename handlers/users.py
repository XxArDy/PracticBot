from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from database import *
from keyboards import *
from main import bot, dp
from misc import DownloadMusic
from states import UserStates


# region commands
@dp.message_handler(Command('start'))
async def start_cmd(message: types.Message):
    await bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}', reply_markup=start_keyboard)


@dp.message_handler(Command('candy'))
async def candy_cmd(message: types.Message):
    await message.reply(text='CANDYYYYYYYYYYYYYYYYYYYYYYY🍫🍭🍬🍭🍩', reply_markup=candy_menu_keyboard)
    prod = await get_product_by_id(1)
    await bot.send_photo(message.chat.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                         caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                 f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))


# endregion

# region text


@dp.message_handler(Text(equals=['Найти музику']), state=None)
async def find_music(message: types.Message):
    await message.answer('Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()


@dp.message_handler(Text(equals=['Вихід']))
async def find_music(message: types.Message):
    await bot.send_message(message.from_user.id, text='Повернули до музики', reply_markup=start_keyboard)


@dp.message_handler(state=UserStates.state)
async def find_music(message: types.Message, state: FSMContext):
    await state.finish()
    down = DownloadMusic(message)
    await down.download()


@dp.message_handler(Text(equals=['Корзина']))
async def show_cart(message: types.Message):
    products = await get_order(message.from_user.id)
    keyboard = await gen_cart(products, message.from_user.id)
    if products:
        await bot.send_message(message.from_user.id, text='Ваші товари в корзині:', reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, text='Корзина пуста', reply_markup=keyboard)

# endregion

# region callbacks


@dp.callback_query_handler(text='continue')
async def continue_music(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Ведіть силку або напишіть назву відео з ютуба:')
    await UserStates.state.set()


@dp.callback_query_handler(callback_data.filter(action='next'))
async def candy_next(callback: types.CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    amount += 1
    prod = await get_product_by_id(amount)
    if prod is not None:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                        caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                                f'\nОпис: {prod.description}'),
            reply_markup=get_keyboard(amount))


@dp.callback_query_handler(callback_data.filter(action='back'))
async def candy_back(callback: types.CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    amount -= 1
    prod = await get_product_by_id(amount)
    if prod is not None:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(media=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                        caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                                f'\nОпис: {prod.description}'), reply_markup=get_keyboard(amount))


@dp.callback_query_handler(callback_data.filter(action='add_to_cart'))
async def candy_add(callback: types.CallbackQuery, callback_data: dict):
    await add_order(callback.from_user.id, int(callback_data['amount']))
    amount = int(callback_data['amount'])
    await callback.message.delete_reply_markup()
    await callback.message.edit_reply_markup(get_keyboard(amount))


@dp.callback_query_handler(text='back_menu')
async def candy_back(callback: types.CallbackQuery):
    prod = await get_product_by_id(1)
    await bot.send_photo(callback.from_user.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                         caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                 f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))


@dp.callback_query_handler(callback_data.filter(action='plus'))
async def candy_plus(callback: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('amount')
    count_in_cart = await get_quantity(callback.message.chat.id, product_id)
    count = 0 if not count_in_cart else sum(j.quantity for j in count_in_cart)
    await update_cart(callback.message.chat.id, product_id, count + 1)
    data = await get_order(callback.from_user.id)
    keyboard = await gen_cart(data, callback.from_user.id)

    await callback.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(callback_data.filter(action='minus'))
async def candy_minus(callback: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('amount')
    count_in_cart = await get_quantity(callback.message.chat.id, product_id)
    count = 0 if not count_in_cart else sum(j.quantity for j in count_in_cart)
    if count == 0:
        await callback.message.answer('Товара нема')
        return 0
    elif count == 1:
        await remove_one_item(callback.message.chat.id, product_id)
    else:
        await update_cart(callback.message.chat.id, product_id, count - 1)
    data = await get_order(callback.from_user.id)
    keyboard = await gen_cart(data, callback.from_user.id)

    await callback.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(callback_data.filter(action='remove'))
async def candy_remove(callback: types.CallbackQuery, callback_data: dict):
    product_id = callback_data.get('amount')
    await remove_one_item(callback.from_user.id, product_id)
    data = await get_order(callback.from_user.id)
    keyboard = await gen_cart(data, callback.from_user.id)

    await callback.message.edit_reply_markup(keyboard)


@dp.callback_query_handler(text='pay')
async def candy_pay(callback: types.CallbackQuery):
    suma = 0
    products = await get_order(callback.from_user.id)
    for i in products:
        prod = await get_product_by_id(i.product_id)
        suma += i.quantity * prod.price

    await bot.send_message(callback.from_user.id, text=f'Ваша сума до оплати:\n{suma}грн', reply_markup=pay_keyboard)


@dp.callback_query_handler(text='accept_pay')
async def candy_accept_pay(callback: types.CallbackQuery):
    await delete_order(callback.from_user.id)
    await bot.send_message(callback.from_user.id, text='Ви успішно оплатили покупку!', reply_markup=continue_buy)


@dp.callback_query_handler(text='continue_buy')
async def candy_continue_buy(callback: types.CallbackQuery):
    prod = await get_product_by_id(1)
    await bot.send_photo(callback.from_user.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                         caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                 f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))


@dp.callback_query_handler(text='exit')
async def candy_exit(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, text='Повернули до музики', reply_markup=start_keyboard)

# endregion

