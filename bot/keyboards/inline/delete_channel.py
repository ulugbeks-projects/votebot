from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def delete_channel_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Kanalni o'chirish", callback_data='delete_channel'))
    return keyboard