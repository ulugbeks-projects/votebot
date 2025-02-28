from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import TelegramAPIError

from bot.loader import dp
from bot.keyboards.inline import vote_options_kb
from bot.utils.db_api.db import create_voteoption_group, create_vote_post
from asgiref.sync import sync_to_async
import logging


# Helper function to reset state and reply with error if needed
async def cancel_and_reset(message: types.Message, state: FSMContext, error_text: str = None):
    await state.finish()
    if error_text:
        await message.answer(error_text, reply_markup=types.ReplyKeyboardRemove())


# Command handler to initiate vote creation
@dp.message_handler(Command("new_vote"), state="*")
async def create_vote_handler(message: types.Message, state: FSMContext):
    await state.finish()  # Clear any existing states

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Keyingisi ➡️", "❌ Bekor qilish")

    await message.answer(
        "📊 So'rovnoma yaratish boshlandi!\n"
        "So'rovnoma uchun rasm yuboring yoki \"Keyingisi ➡️\" tugmasini bosing.",
        reply_markup=keyboard
    )
    await state.set_state("create_vote")


# Handler to process image or move to next step
@dp.message_handler(state="create_vote", content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_vote_image_or_skip(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel_and_reset(message, state, "❌ So'rovnoma yaratish bekor qilindi.\n"
                               "Qaytadan /new_vote buyrug'ini bosing yoki /start buyrug'ini bosing.")
        return

    if message.text == "Keyingisi ➡️":
        await state.update_data(photo_id=None)
        await message.answer("✏️ So'rovnoma matnini yuboring.", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        await state.update_data(photo_id=message.photo[-1].file_id)
        await message.answer("📸 Rasm qabul qilindi.\n✏️ Endi so'rovnoma matnini yuboring.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("⚠️ Noto'g'ri buyruq! Iltimos, rasm yuboring yoki \"Keyingisi ➡️\" tugmasini bosing.")
        return

    await state.set_state("vote_text")


# Handler to receive the vote text
@dp.message_handler(state="vote_text", content_types=types.ContentType.TEXT)
async def get_vote_text_handler(message: types.Message, state: FSMContext):
    await state.update_data(vote_text=message.text.strip())
    await message.answer(
        "📄 So'rovnoma matni qabul qilindi.\n"
        "✍️ So'rovnoma uchun variantlarni yuboring.\n\n"
        "<i>*Variantlar har biri yangi qatorda yozilishi kerak.</i>",
        parse_mode="HTML"
    )
    await state.set_state("vote_options")


# Handler to receive and process vote options
@dp.message_handler(state="vote_options", content_types=types.ContentType.TEXT)
async def get_vote_options_handler(message: types.Message, state: FSMContext):
    options = [opt.strip() for opt in message.text.strip().split("\n") if opt.strip()]

    if len(options) < 2:
        await message.answer("⚠️ Kamida 2 ta variant kiritishingiz kerak! Qaytadan kiriting.")
        return

    await state.update_data(options=options)

    # Process options and create vote options group
    try:
        option_group_id, option_items = await create_voteoption_group(options)
    except Exception as e:
        logging.error(f"Failed to create vote option group: {e}")
        await cancel_and_reset(message, state, "⚠️ Variantlarni saqlashda xatolik yuz berdi.")
        return

    await state.update_data(option_group_id=option_group_id, option_items=option_items)

    data = await state.get_data()

    # Create vote post
    try:
        vote_post = await create_vote_post(
            user_id=message.from_user.id,
            media_type="photo" if data.get("photo_id") else "none",
            media_id=data.get("photo_id"),
            caption=data["vote_text"],
            message_id=message.message_id,
            options_group_id=option_group_id
        )
        post_id = await sync_to_async(lambda: vote_post.id)()

    except Exception as e:
        logging.error(f"Failed to create vote post: {e}")
        await cancel_and_reset(message, state, "⚠️ So'rovnoma saqlashda xatolik yuz berdi.")
        return

    # Send vote preview to user
    try:
        if data.get("photo_id"):
            await message.answer_photo(
                photo=data["photo_id"],
                caption=data["vote_text"],
                reply_markup=vote_options_kb(option_items, post_id)
            )
        else:
            await message.answer(
                data["vote_text"],
                reply_markup=vote_options_kb(option_items, post_id)
            )

        await message.answer(
            "✅ So'rovnoma yaratildi.\n"
            "Kanalga yuborish uchun /votes buyrug'ini bosing."
        )

    except TelegramAPIError as e:
        logging.error(f"Telegram error while sending vote preview: {e}")
        await cancel_and_reset(message, state, "⚠️ Telegramga so'rovnoma yuborishda xatolik yuz berdi.")
        return

    await state.finish()
