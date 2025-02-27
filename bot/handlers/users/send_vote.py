from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.loader import dp
from bot.utils.db_api.db import get_unsend_voteposts, get_send_post_info, change_votepost_status
from bot.keyboards.inline import get_unsend_voteposts_keyboard, unsend_voteposts_callback
from bot.keyboards.inline import vote_options_kb


async def send_vote(post_id):
    response = await get_send_post_info(post_id)
    if response:
        channel = response.get('channel')
        media_type = response.get('media_type')
        media_id = response.get('media_id')
        caption = response.get('caption')
        message_id = response.get('message_id')
        options = response.get('options')
        
        if media_type == 'photo':
            message = await dp.bot.send_photo(channel, media_id, caption=caption, reply_markup=vote_options_kb(options))
        
        elif media_type == 'none':
            message = await dp.bot.send_message(channel, caption, reply_markup=vote_options_kb(options))
        
        await change_votepost_status(post_id, 'published', message.message_id)



@dp.message_handler(Command("send_vote"))
async def send_vote_handler(message: types.Message):
    user_id = message.from_user.id
    voteposts = await get_unsend_voteposts(user_id)
    if voteposts:
        await message.answer("Tanlang", reply_markup=get_unsend_voteposts_keyboard(voteposts))
    else:
        await message.answer("Sizda hali so'rovnomalar mavjud emas!\n"
                             "Avval so'rovnoma yarating!\n"
                             "So'rovnoma yaratish uchun /create_vote")
        return

@dp.callback_query_handler(unsend_voteposts_callback.filter())
async def get_unsend_post_id(call: types.CallbackQuery, callback_data: dict):
    post_id = callback_data.get("id")
    await send_vote(post_id)
    await call.message.edit_text("So'rovnoma kanalga yuborildi✅")
    