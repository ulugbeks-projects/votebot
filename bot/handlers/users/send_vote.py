from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.loader import dp
from bot.utils.db_api.db import get_unsend_voteposts, get_send_post_info, change_votepost_status, get_channel
from bot.keyboards.inline import get_unsend_voteposts_keyboard, unsend_voteposts_callback
from bot.keyboards.inline import vote_options_kb
import logging


async def send_vote(post_id):
    response = await get_send_post_info(post_id)
    if response:
        channel = response.get('channel')
        media_type = response.get('media_type')
        media_id = response.get('media_id')
        caption = response.get('caption')
        options = response.get('options')
        
        if media_type == 'photo':
            message = await dp.bot.send_photo(channel, media_id, caption=caption, reply_markup=vote_options_kb(options, post_id))
            await message.edit_caption(caption+"\n"+message.link("Ulashish uchun link"), reply_markup=vote_options_kb(options, post_id))
        elif media_type == 'none':
            message = await dp.bot.send_message(channel, caption, reply_markup=vote_options_kb(options, post_id))
            await message.edit_text(caption+"\n\n"+message.link("Ulashish uchun link"), reply_markup=vote_options_kb(options, post_id), disable_web_page_preview=True)
        
        await change_votepost_status(post_id, 'published', message.message_id)
        



@dp.message_handler(Command("votes"))
async def send_vote_handler(message: types.Message):
    user_id = message.from_user.id
    user_channel = await get_channel(user_id)
    if not user_channel:
        await message.answer("Sizda kanal mavjud emas!\n"
                             "Kanal qo'shish uchun /add_channel buyrug'ini bosing")
        return
    voteposts = await get_unsend_voteposts(user_id)
    if voteposts:
        await message.answer("Kanalga yubormoqchi bo'lgan so'rovnomani tanlang👇", reply_markup=get_unsend_voteposts_keyboard(voteposts))
    else:
        await message.answer("Sizda hali so'rovnomalar mavjud emas!\n"
                             "Avval so'rovnoma yarating!\n"
                             "So'rovnoma yaratish uchun /new_vote buyrug'ini bosing")
        return

@dp.callback_query_handler(unsend_voteposts_callback.filter())
async def get_unsend_post_id(call: types.CallbackQuery, callback_data: dict):
    post_id = callback_data.get("id")
    await send_vote(post_id)
    await call.message.edit_text("So'rovnoma kanalga yuborildi✅\n"
                                 "Bosh menyu uchun /start buyrug'ini bosing")
    