from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

kall = CallbackData('vote', 'action', 'amount')  # post:<action>:<amount>

continue_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити', callback_data='continue'))

def get_keyboard(amount):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬅️', callback_data=kall.new(action='back',amount=amount)),
    InlineKeyboardButton(text='В корзину', callback_data='add_to_cart'),
InlineKeyboardButton(text='➡️', callback_data=kall.new(action='next',amount=amount)))
