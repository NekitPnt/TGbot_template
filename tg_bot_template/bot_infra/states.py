from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class Form(StatesGroup):
    name = State()
    username = State()
