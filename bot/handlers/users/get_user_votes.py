from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from bot.loader import dp, bot
from bot.keyboards.inline import vote_options_cb, vote_options_kb
from asgiref.sync import sync_to_async
from botapp.models import BotUser
from bot.utils.db_api.db import user_vote
import logging


@dp.callback_query_handler(vote_options_cb.filter())
async def process_vote_callback(call: types.CallbackQuery, callback_data: dict):
    option_id = callback_data['option_id']
    post_id = callback_data['post_id']
    user = call.from_user

    # Fetch or create BotUser record
    bot_user, created = await sync_to_async(BotUser.objects.get_or_create)(
        user_id=str(user.id),
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'language_code': user.language_code or 'uz'
        }
    )

    # Check if user is subscribed to the channel
    try:
        chat_member = await bot.get_chat_member(call.message.chat.id, user.id)
        is_subscribed = chat_member.status in [
            types.ChatMemberStatus.CREATOR,
            types.ChatMemberStatus.ADMINISTRATOR,
            types.ChatMemberStatus.MEMBER
        ]
    except Exception as e:
        logging.error(f"Failed to fetch chat member {user.id} for chat {call.message.chat.id}: {e}")
        is_subscribed = False  # Default to False if something goes wrong

    # Process the user's vote
    response = await user_vote(bot_user, post_id, option_id, is_subscribed)

    if response:
        if response['status']:
            try:
                # Update the vote buttons to show new counts
                await bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=vote_options_kb(response['options'], post_id)
                )
                await call.answer(response['message'], show_alert=False)
            except MessageNotModified:
                pass  # Ignore if nothing actually changed
        else:
            await call.answer(response['message'], show_alert=True)
    else:
        await call.answer('Xatolik yuz berdi', show_alert=True)
