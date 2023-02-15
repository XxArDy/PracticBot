from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    state = State()


class QuantityState(StatesGroup):
    state = State()