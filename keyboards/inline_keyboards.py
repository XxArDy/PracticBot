from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


callback_data = CallbackData('vote', 'action', 'amount')

continue_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити', callback_data='continue'))


def get_keyboard(amount):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='⬅️', callback_data=callback_data.new(action='back', amount=amount)),
        InlineKeyboardButton(text='В корзину', callback_data='add_to_cart'),
        InlineKeyboardButton(text='➡️', callback_data=callback_data.new(action='next', amount=amount)))
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬅️', callback_data=callbackdata.new(action='back', amount=amount)),
                                      InlineKeyboardButton(text='В корзину', callback_data=callbackdata.new(action='add_to_cart', amount=amount)),
                                      InlineKeyboardButton(text='➡️', callback_data=callbackdata.new(action='next',amount=amount)))
