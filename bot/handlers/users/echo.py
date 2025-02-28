from aiogram import types

from bot.loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Noto'g'ri buyruq kiritdingiz!\n"
                         "Yordam uchun /help buyrug'ini kiriting")
