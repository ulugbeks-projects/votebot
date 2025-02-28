from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.utils.db_api.db import add_channel, get_channel
from aiogram import Bot
from aiogram.types import ChatMemberStatus
import logging


async def is_bot_admin(bot: Bot, channel: str) -> bool:
    """
    Check if the bot is an admin in a public or private channel.

    Supports:
    - Public channels (e.g., @channelname)
    - Private channels (e.g., -100xxxxx)
    - Private invite links (e.g., https://t.me/+xxxxx) - must convert to chat object first
    """
    try:
        if channel.startswith("https://t.me/"):
            try:
                chat = await bot.get_chat(channel)
                channel = chat.id  # Convert to -100xxxxxxx
            except Exception as e:
                logging.error(f"Failed to fetch chat from invite link: {e}")
                return False

        chat_member = await bot.get_chat_member(channel, bot.id)
        return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER, ChatMemberStatus.CREATOR]
    except Exception as e:
        logging.error(f"Error checking bot admin status for {channel}: {e}")
        return False


@dp.message_handler(Command('add_channel'), state="*")
async def add_channel_handler(message: types.Message, state: FSMContext):
    # first disable all states
    await state.finish()

    # get user channel
    channel = await get_channel(message.from_user.id)

    # if user has channel
    if channel:
        await message.answer("Sizda allaqachon kanal bor\n"
                             "Ko'rish uchun /my_channel buyrug'ini bosing")
        return
    
    # get channel from user
    await message.answer("Kanal username yoki id sini kiriting")
    await state.set_state("channel")


@dp.message_handler(state="channel")
async def get_channel_handler(message: types.Message, state: FSMContext):
    channel = message.text.strip()

    if channel.startswith("https://t.me/+"):
        await message.answer("❌ Bot private kanalga taklif havolasi orqali kira olmaydi.\n"
                             "Iltimos, botni kanalingizga admin sifatida qo'shing va kanal ID yoki username-ni yuboring.")
        return

    if not (channel.startswith("@") or channel.startswith("-100")):
        await message.answer("❌ Noto'g'ri format. Iltimos, kanal username (@channelname) yoki ID (-100...) ni yuboring.")
        return

    try:
        is_admin = await is_bot_admin(bot, channel)

        if not is_admin:
            await message.answer("❌ Bot ushbu kanalda admin emas. Iltimos, botga admin huquqlarini bering va qayta urinib ko'ring.")
            return

        added_channel, created = await add_channel(channel=channel, user_id=message.from_user.id, is_admin=True)

        if created:
            await message.answer("✅ Kanal muvaffaqiyatli qo'shildi!\n"
                                 "Ko'rish uchun /my_channel buyrug'ini bosing\n"
                                 "Yangi so'rovnoma yaratish uchun /new_vote buyrug'ini bosing\n"
                                 "So'rovnoma ro'yxatini ko'rish uchun /votes buyrug'ini bosing")
        else:
            await message.answer("⚠️ Bu kanal allaqachon qo'shilgan.\n"
                                 "Ko'rish uchun /my_channel buyrug'ini bosing")

    except Exception as e:
        logging.error(f"Error while adding channel: {e}")
        await message.answer("⚠️ Kanal qo'shish jarayonida xatolik yuz berdi. Keyinroq qayta urinib ko'ring yoki adminstratorga murojaat qiling.\n"
                             "Admin: @Abdulazizov_Ulugbek")

    await state.finish()

