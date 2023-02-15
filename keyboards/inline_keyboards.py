from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

callbackdata = CallbackData('vote', 'action', 'amount')  # post:<action>:<amount>

continue_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити', callback_data='continue'))

def get_keyboard(amount):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬅️', callback_data=callbackdata.new(action='back', amount=amount)),
                                      InlineKeyboardButton(text='В корзину', callback_data=callbackdata.new(action='add_to_cart', amount=amount)),
                                      InlineKeyboardButton(text='➡️', callback_data=callbackdata.new(action='next',amount=amount)))
