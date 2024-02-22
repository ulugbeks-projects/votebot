from aiogram import types
from asgiref.sync import sync_to_async
from bot.filters import IsGroup
from bot.loader import dp
from botapp.models import GroupMembers, Groups, TgUser
from django.utils import timezone


@sync_to_async
def add_group_member(group, user, invited=None, left=None, is_active=True):
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
    joined = timezone.now()

    # Use get_or_create to either retrieve an existing instance or create a new one
    group_member, created = GroupMembers.objects.get_or_create(
        group=group,
        user=user,
        invited=invited,
        left=left,
        is_active=is_active,
        defaults={'joined': joined}  # Set the 'joined' field only if the instance is newly created
    )

    return group_member


@sync_to_async
def get_group(group_id):
    try:
        group = Groups.objects.get(group_id=group_id)
        return group
    except Groups.DoesNotExist:
        return None


@sync_to_async
def get_tg_user(tg_id, username, first_name, last_name):
    try:
        user, created = TgUser.objects.get_or_create(
            tg_id=tg_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'is_active': False
            }
        )
        return user
    except TgUser.DoesNotExist:
        return None


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_members(message: types.Message):
    for new_member in message.new_chat_members:
        if new_member.id == message.from_user.id:
            user = await get_tg_user(new_member.id, new_member.username, new_member.first_name, new_member.last_name)
            group = await get_group(message.chat.id)
            if user and group:
                await add_group_member(group=group, user=user)
                await message.reply(f"{new_member.get_mention(as_html=True)} guruhga qo'shildi👤")
        else:
            user = await get_tg_user(new_member.id, new_member.username, new_member.first_name, new_member.last_name)
            invited = await get_tg_user(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name
            )
            group = await get_group(message.chat.id)
            if user and group:
                await add_group_member(group=group, user=user, invited=invited)
                await message.reply(f"{message.from_user.get_mention(as_html=True)} qo'shdi: {new_member.get_mention(as_html=True)}")
