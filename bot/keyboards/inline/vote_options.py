from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


vote_options_cb = CallbackData("vote", "option_id")

def vote_options_kb(options: list):
    kb = InlineKeyboardMarkup(row_width=1)
    for option in options:
        kb.add(InlineKeyboardButton(text=f"{option} | 0", callback_data=vote_options_cb.new(option_id=option.id)))
    return kb