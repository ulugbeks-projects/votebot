from aiogram import types
from asgiref.sync import sync_to_async
from bot.filters import IsGroup
from bot.loader import dp
from botapp.models import GroupMembers, Groups, TgUser
from django.utils import timezone
from bot.handlers.groups.user_join import add_group_member, get_group, get_tg_user


@sync_to_async
def remove_group_member(group, user, invited=None, left=None, is_active=False):
    """
    Add a group member.

    Parameters:
    - group: The group to which the user belongs (Groups object).
    - user: The user who is a member of the group (TgUser object).
    - invited: The user who invited the member (TgUser object or None).
    - left: The datetime when the user left the group (datetime object or None).
    - is_active: Boolean indicating if the member is active (True or False).

    Returns:
    - The created or retrieved GroupMembers instance.
    """
    # Use timezone.now() to get the current datetime
    left = timezone.now()

    # Use get_or_create to either retrieve an existing instance or create a new one
    group_member, created = GroupMembers.objects.get_or_create(
        group=group,
        user=user,
        invited=invited,
        left=left,
        is_active=is_active,
        defaults={'left': left}  # Set the 'joined' field only if the instance is newly created
    )

    return group_member


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def left_members(message: types.Message):
    user = await get_tg_user(
        message.left_chat_member.id,
        message.left_chat_member.username,
        message.left_chat_member.first_name,
        message.left_chat_member.last_name
    )
    group = await get_group(message.chat.id)
    if user and group:
        await remove_group_member(group=group, user=user)
        print("success")

    if message.left_chat_member.id == message.from_user.id:
        await message.reply(f"{message.left_chat_member.get_mention(as_html=True)} guruhdan chiqdi!")
    else:
        await message.reply(f"{message.from_user.get_mention(as_html=True)} chiqarib yubordi: {message.left_chat_member.get_mention(as_html=True)}")
