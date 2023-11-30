from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    """ Функция, генерирующая клавиатуру для страницы книги. """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[
        InlineKeyboardButton(
            text=LEXICON.get(button, button),
            callback_data=button
        ) for button in buttons
    ])
    return kb_builder.as_markup()

