from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.utils.db_api.db import get_or_create_user

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    user, created = await get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    if created:
        await message.answer("Assalomu alaykum!\n"
                             "Bizning so'rovnoma yaratish botimizga xush kelibsiz!\n")
    else:
        await message.answer("Salom!\n"
                             "Sizni qayta ko'rishdan xursandmiz!\n")
    


