from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


unsend_voteposts_callback = CallbackData("post_id", "id")

def get_unsend_voteposts_keyboard(voteposts: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for votepost in voteposts:
        button = InlineKeyboardButton(
            text=f"{votepost.caption}",
            callback_data=unsend_voteposts_callback.new(id=votepost.id)
        )
        keyboard.insert(button)
    return keyboard