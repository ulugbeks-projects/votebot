from aiogram import types
from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.utils.db_api.db import add_channel, get_channel
from aiogram import Bot
from aiogram.types import ChatMemberStatus


async def is_bot_admin(bot: Bot, channel: str) -> bool:
    """Check if the bot is an admin in a public or private channel."""
    try:
        chat_member = await bot.get_chat_member(channel, bot.id)
        return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"Error: {e}")
        return False


@dp.message_handler(Command('add_channel'), state="*")
async def add_channel_handler(message: types.Message, state: FSMContext):
    # first disable all states
    await state.finish()

    # get user channel
    channel = await get_channel(message.from_user.id)

    # if user has channel
    if channel:
        await message.answer("Sizda allaqachon kanal bor")
        return
    
    # get channel from user
    await message.answer("Kanal username yoki id sini kiriting")
    await state.set_state("channel")


@dp.message_handler(state="channel")
async def get_channel_handler(message: types.Message, state: FSMContext):
    # get channel from user
    channel = message.text

    # check if channel is valid
    if not channel.startswith("@") and not channel.isdigit():
        await message.answer("Kanal username yoki id sini kiriting")
        return
    
    # check if bot is admin in channel
    is_admin = await is_bot_admin(bot, channel)
    if not is_admin:
        await message.answer("Bot kanalda admin emas")
        return

    # add channel to user
    channel, created = await add_channel(channel=channel, user_id=message.from_user.id, is_admin=True)

    # if channel added
    if created:
        await message.answer("Kanal qo'shildi")
    else:
        await message.answer("Kanal qo'shilmadi")

    # finish state
    await state.finish()
