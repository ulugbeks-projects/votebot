from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from bot.loader import dp, bot
from bot.keyboards.inline import vote_options_cb, vote_options_kb
from asgiref.sync import sync_to_async
from botapp.models import BotUser
from bot.utils.db_api.db import user_vote


@dp.callback_query_handler(vote_options_cb.filter())
async def process_vote_callback(call: types.CallbackQuery, callback_data: dict):
    option_id = callback_data['option_id']
    post_id = callback_data['post_id']
    user = call.from_user

    # Get or create BotUser
    bot_user, created = await sync_to_async(BotUser.objects.get_or_create)(
        user_id=str(user.id),
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'language_code': user.language_code or 'uz'
        }
    )

    chat_member = await bot.get_chat_member(call.message.chat.id, user.id)

    is_subscribed = chat_member.status in [types.ChatMemberStatus.CREATOR, types.ChatMemberStatus.ADMINISTRATOR, types.ChatMemberStatus.MEMBER]

    response = await user_vote(bot_user, post_id, option_id, is_subscribed)

    if response:
        if response['status']:
            try:
                await bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=vote_options_kb(response['options'], post_id)
                )
                await call.answer(response['message'], show_alert=False)
            except MessageNotModified:
                pass
        else:
            await call.answer(response['message'], show_alert=True)
    else:
        await call.answer('Error', show_alert=True)
    


    