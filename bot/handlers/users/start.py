from aiogram import types
from aiogram.utils.callback_data import CallbackData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.keyboards.default import home
from bot.loader import dp
from asgiref.sync import sync_to_async
from botapp.models import TgUser
from botapp.models import Message


call_data = CallbackData("page", "id")


# foydalanuchilarni bazaga qo'shish
@sync_to_async
def add_user(username, first_name, last_name, tg_id, is_active=True):
    try:
        user = TgUser.objects.get(tg_id=tg_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = is_active
        user.save()
    except TgUser.DoesNotExist:
        user = TgUser.objects.create(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
    return user


@sync_to_async
def all_messages():
    all_messages = Message.objects.all()
    return list(all_messages)


async def show_message(chat_id, message_id=0):
    messages = await all_messages()
    if message_id > len(messages)-1:
        await dp.bot.send_message(chat_id, "Yakunlandi")
        return False
    keyboard = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="<<", callback_data=call_data.new(id=message_id-1)),
                InlineKeyboardButton(text=">>", callback_data=call_data.new(id=message_id + 1))
            ]
        ]
    )
    message = messages[message_id]
    if message.image and message.video:
        media = types.MediaGroup()
        media.attach_photo(types.InputFile(message.image.path))
        media.attach_video(types.InputFile(message.video.path), caption=message.text)
        await dp.bot.send_chat_action(chat_id, types.ChatActions.UPLOAD_VIDEO)
        await dp.bot.send_media_group(chat_id, media)
        await dp.bot.send_message(chat_id, "Tanlang", reply_markup=keyboard)

    elif message.image:
        with open(message.image.path, "rb") as image:
            await dp.bot.send_chat_action(chat_id, types.ChatActions.UPLOAD_PHOTO)
            await dp.bot.send_photo(chat_id, image, caption=message.text, reply_markup=keyboard)

    elif message.video:
        await dp.bot.send_chat_action(chat_id, types.ChatActions.UPLOAD_VIDEO)
        with open(message.video.path, "rb") as video:
            await dp.bot.send_video(chat_id, video, caption=message.text)

    elif message.text:
        await dp.bot.send_chat_action(chat_id, types.ChatActions.TYPING)
        await dp.bot.send_message(chat_id, message.text, reply_markup=keyboard)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # userni bazaga qo'shish agar avval qo'shilmagan bo'lsa qo'shilgan bo'lsa ma'lumotlarni yangilanadi
    await add_user(message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.id)
    # salomlashish xabari
    await message.answer(f"Salom, {message.from_user.id}!")
    await show_message(message.chat.id)


@dp.callback_query_handler(call_data.filter())
async def pagination(call: types.CallbackQuery):
    page = call.data
    print(page)
    await call.message.delete()
    await show_message(chat_id=call.message.chat.id, message_id=int(call.data[5:]))



