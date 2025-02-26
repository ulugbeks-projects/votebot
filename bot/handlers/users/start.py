from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.utils.db_api.db import get_or_create_user

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # salomlashish xabari
    await message.answer(f"Salom, {message.from_user.id}!")



