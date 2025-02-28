from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from bot.loader import dp
from bot.keyboards.inline import vote_options_kb
from bot.utils.db_api.db import create_voteoption_group, create_vote_post
from asgiref.sync import sync_to_async

# Command handler to initiate vote creation
@dp.message_handler(Command("create_vote"), state="*")
async def create_vote_handler(message: types.Message, state: FSMContext):
    await state.finish()  # Reset any existing state
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Keyingisi ➡️", "❌ Bekor qilish")
    
    await message.answer("So'rovnoma yaratish boshlandi!\n"
                         "So'rovnoma uchun rasm yuboring (*ixtiyoriy*)", 
                         reply_markup=keyboard)
    await state.set_state("create_vote")

# Handler for processing image or moving to next step
@dp.message_handler(state="create_vote", content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_vote_image_or_skip(message: types.Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await message.answer("So'rovnoma yaratish bekor qilindi!", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    
    if message.text == "Keyingisi ➡️":
        await state.update_data(photo_id=None)
        await message.answer("So'rovnoma matnini yuboring.", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        await state.update_data(photo_id=message.photo[-1].file_id)
        await message.answer("Rasm qabul qilindi✅\nSo'rovnoma matnini yuboring.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Noto'g'ri buyruq!", reply_markup=types.ReplyKeyboardRemove())
        return
    
    await state.set_state("vote_text")

# Handler to receive the vote text
@dp.message_handler(state="vote_text", content_types=types.ContentType.TEXT)
async def get_vote_text_handler(message: types.Message, state: FSMContext):
    await state.update_data(vote_text=message.text)
    await message.answer("So'rovnoma matni qabul qilindi✅\n"
                         "So'rovnoma uchun variantlarni yuboring!\n"
                         "*Variantlar har biri yangi qatorda yozilishi kerak*", 
                         parse_mode="HTML")
    await state.set_state("vote_options")

# Handler to receive and process vote options
@dp.message_handler(state="vote_options", content_types=types.ContentType.TEXT)
async def get_vote_options_handler(message: types.Message, state: FSMContext):
    options = [opt.strip() for opt in message.text.split("\n") if opt.strip()]
    if not options:
        await message.answer("Variantlar bo'sh bo'lishi mumkin emas! Qaytadan kiriting.")
        return
    
    await state.update_data(options=options)
    data = await state.get_data()
    
    option_group_id, option_items = await create_voteoption_group(options)
    await state.update_data(option_group_id=option_group_id, option_items=option_items)
    
    await state.update_data(message_id=message.message_id)
    vote_post = await create_vote_post(
        user_id=message.from_user.id,
        media_type="photo" if data.get("photo_id") else "none",
        media_id=data.get("photo_id"),
        caption=data["vote_text"],
        message_id=message.message_id,
        options_group_id=option_group_id
    )
    
    post_id = await sync_to_async(lambda: vote_post.id)()

    if data.get("photo_id"):
        await message.answer_photo(
            photo=data["photo_id"], caption=data["vote_text"], reply_markup=vote_options_kb(option_items, post_id)
        )
    else:
        await message.answer(data["vote_text"], reply_markup=vote_options_kb(option_items, post_id))
    
    if vote_post:
        await message.answer("So'rovnoma yaratildi✅\nKanalga yuborish uchun /send_vote buyrug'ini bosing")
    else:
        await message.answer("Xatolik yuz berdi! So'rovnoma yaratish bekor qilindi!")

    await state.finish()

