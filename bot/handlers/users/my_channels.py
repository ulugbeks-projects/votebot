from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.loader import dp
from bot.utils.db_api.db import get_channel, delete_channel
from bot.keyboards.inline import delete_channel_keyboard


@dp.message_handler(Command("my_channel"))
async def my_channel_handler(message: types.Message):

    channel = await get_channel(message.from_user.id)
    if channel:
        await message.answer(f"Sizning kanal: {channel}", reply_markup=delete_channel_keyboard())
    else:   
        await message.answer("Sizda kanal mavjud emas!\nKanalni qo'shish uchun /add_channel buyrug'ini bering")


@dp.callback_query_handler(text="delete_channel")
async def delete_channel_handler(call: types.CallbackQuery):
    is_deleted = await delete_channel(call.from_user.id)

    if is_deleted:
        await call.message.answer("Kanal muvaffaqiyatli o'chirildi!")
        await call.message.delete_reply_markup()
    else:
        await call.message.answer("Kanal o'chirishda xatolik!")
        await call.message.delete_reply_markup()

    