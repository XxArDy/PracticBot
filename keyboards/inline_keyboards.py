from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

continue_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити', callback_data='continue'))
shop_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬅️', callback_data='back'),
    InlineKeyboardButton(text='В корзину', callback_data='add_to_cart'),
InlineKeyboardButton(text='➡️', callback_data='next'))
