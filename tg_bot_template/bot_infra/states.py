from aiogram.dispatcher.filters.state import State, StatesGroup
from dataclasses import dataclass


@dataclass
class UserFormData:
    name: str
    info: str
    photo: str


class UserForm(StatesGroup):  # type: ignore[misc]
    name = State()
    info = State()
    photo = State()
