from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("votes", "Barcha so'rovnomalaringiz"),
            types.BotCommand("new_vote", "Yangi so'rovnoma yaratish"),
            types.BotCommand("add_channel", "Kanal qo'shish"),
            types.BotCommand("my_channel", "Sizning kanalingiz"),
        ]
    )
