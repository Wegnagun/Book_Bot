from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import (
    create_bookmark_keyboard, create_edit_keyboard
)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from servises.file_handling import book

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """ Хендлер обработки команды /start. """
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """ Хендлер обработки команды /help. """
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    """ Хендлер обработки команды /beginning. """
    user_id = message.from_user.id
    users_db[user_id]['page'] = 1
    text = book[users_db[user_id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[user_id]["page"]}/{len(book)}'
        )
    )


@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    """ Хендлер обработки команды /continue. """
    user_id = message.from_user.id
    text = book[users_db[user_id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[user_id]["page"]}/{len(book)}',
            'forward'
        )
    )


@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    """ Хендлер обработки команды /bookmarks. """
    user_id = message.from_user.id
    if users_db[user_id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmark_keyboard(
                *users_db[user_id]['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия кнопки 'вперед'. """
    user_id = callback.from_user.id
    if users_db[user_id]['page'] < len(book):
        users_db[user_id]['page'] += 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия кнопки 'назад'. """
    user_id = callback.from_user.id
    if users_db[user_id]['page'] > 1:
        users_db[user_id]['page'] -= 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(
    lambda x: "/" in x.data and x.data.replace("/", "").isdigit()
)
async def process_page_press(callback: CallbackQuery):
    """ Хендлер обработки на нажатие кнопки с номером страницы. """
    user_id = callback.from_user.id
    users_db[user_id]['bookmarks'].add(
        users_db[user_id]['page']
    )
    await callback.answer('Страница добавлена в закладки!')


@router.callback_query(IsDigitCallbackData())
async def process_bookmarks_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия кнопки с закладками. """
    user_id = callback.from_user.id
    text = book[int(callback.data)]
    users_db[user_id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[user_id]["page"]}/{len(book)}',
            'forward'
        )
    )
    await callback.answer()


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия кнопки "редактировать". """
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия кнопки "отменить". """
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData)
async def process_del_bookmark_press(callback: CallbackQuery):
    """ Хендлер обработки нажатия закладки для удаления. """
    user_id = callback.from_user.id
    users_db[user_id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[user_id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[user_id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
