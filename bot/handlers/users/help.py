import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from bot.loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    logging.info(f"Help command received from user: {message.from_user.id}")

    text = (
        "Bot sizga so'rovnoma yaratishga yordam beradi",
        "Bunda siz botni kanalingizga admin qilishingiz kerak",
        "Shunda bot so'rovnomani kanalingizga yuboradi va boshqalar sizni kanalingizga a'zo bo'lmagan bo'lsa ovoz berolmaydilar",
        "\n\n\n",
        "Botdagi barcha buyruqlar:",
        "/start - Botni ishga tushirish",
        "/help - Yordam",
        "/new_vote - So'rovnoma yaratish",
        "/votes - Yuborilmagan so'rovnomalarni ko'rish",
        "/add_channel - Kanal qo'shish",
        "/my_channel - Mening kanallarim",
    )

    await message.answer("\n".join(text))

    logging.info(f"Help message sent to user: {message.from_user.id}")
