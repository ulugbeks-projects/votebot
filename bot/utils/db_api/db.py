from asgiref.sync import sync_to_async
from botapp.models import BotUser, BotUserChannel, VoteOptionItem, VoteOption, VotePost, Vote
import logging
from aiogram.types import ChatMemberStatus
from bot.loader import bot

@sync_to_async 
def get_or_create_user(user_id, first_name: str, last_name: str|None, username:str|None):
    user, created = BotUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
    )
    return user, created



@sync_to_async
def add_channel(user_id, channel, is_admin=False):
    try:
        user = BotUser.objects.get(user_id=user_id)
        channel, created = BotUserChannel.objects.get_or_create(user=user, defaults={'channel': channel, 'is_admin': is_admin})
        return channel, created
    except BotUser.DoesNotExist:
        return None, False
    
    except Exception as e:
        return None, False
    

@sync_to_async
def get_channel(user_id):
    try:
        user = BotUser.objects.get(user_id=user_id)
        channels = BotUserChannel.objects.get(user=user)
        return channels
    except BotUser.DoesNotExist:
        return None
    except Exception as e:
        return None


@sync_to_async
def delete_channel(user_id):
    try:
        user = BotUser.objects.get(user_id=user_id)
        channel = BotUserChannel.objects.get(user=user)
        channel.delete()
        return True
    except BotUser.DoesNotExist:
        return False
    except Exception as e:
        return False


@sync_to_async
def create_voteoption_group(options: list):
    vote_option = VoteOption.objects.create()
    for option in options:
        vote_option_item = VoteOptionItem.objects.create(title=option)
        vote_option.items.add(vote_option_item)
    return vote_option.id, list(vote_option.items.all())


@sync_to_async
def create_vote_post(user_id, media_type, media_id, caption, message_id, options_group_id, status='draft'):
    try:
        user = BotUser.objects.get(user_id=user_id)
        vote_option = VoteOption.objects.get(id=options_group_id)
        vote_post = VotePost.objects.create(
            user=user,
            media_type=media_type,
            media_id=media_id,
            caption=caption,
            message_id=message_id,
            options=vote_option,
            status=status
        )
        return vote_post
    except Exception as e:
        logging.error(e)
        return None
    

@sync_to_async
def get_unsend_voteposts(user_id):

    try:
        user = BotUser.objects.get(user_id=user_id)
        vote_posts = VotePost.objects.filter(user=user, status='draft').order_by('-created_at')
        if vote_posts:
            return list(vote_posts)
        return None
    except Exception as err:
        logging.error(err)
        return None


@sync_to_async
def get_send_post_info(post_id):
    try:
        response = {}
        post = VotePost.objects.get(id=post_id)
        channel = BotUserChannel.objects.get(user=post.user)
        response['channel'] = channel.channel
        response['media_type'] = post.media_type
        response['media_id'] = post.media_id
        response['caption'] = post.caption
        response['message_id'] = post.message_id
        response['options'] = list(post.options.items.all())
        return response
    except Exception as err:
        logging.error(err)
        return None
    

@sync_to_async
def change_votepost_status(post_id, status, message_id: str|None):
    try:
        post = VotePost.objects.get(id=post_id)
        post.status = status
        post.message_id = message_id
        post.save()
        return True
    except Exception as e:
        logging.error(e)
        return False


@sync_to_async
def user_vote(bot_user, post_id, option_id, is_subscribed):
    """
    Allows a user to vote only if they are subscribed to the required channel.

    Args:
        bot_user (BotUser): The user object.
        post_id (int): The ID of the vote post.
        option_id (int): The ID of the option user is voting for.
        is_subscribed (bool): Whether the user is verified as subscribed to the channel (from outside).

    Returns:
        dict: Response including status, message, options, and vote object if successful.
    """
    response = {}

    if not is_subscribed:
        response['message'] = 'Ovoz berish uchun avval kanalga obuna bo‘ling!'
        response['status'] = False
        return response

    try:
        post = VotePost.objects.get(id=post_id)
        option = VoteOptionItem.objects.get(id=option_id)

        # Check if the user has already voted on this post
        if Vote.objects.filter(user=bot_user, post=post).exists():
            response['message'] = 'Siz allaqachon ovoz bergansiz!'
            response['status'] = False
        else:
            # Create a new vote record
            vote = Vote.objects.create(
                user=bot_user,
                post=post,
                option=option
            )

            response['message'] = 'Ovoz berildi'
            response['status'] = True
            response['options'] = list(post.options.items.all())
            response['vote'] = vote

        return response

    except VotePost.DoesNotExist:
        logging.error(f"VotePost with id {post_id} does not exist.")
        response['message'] = 'Ovoz berish uchun post topilmadi.'
        response['status'] = False
        return response

    except VoteOptionItem.DoesNotExist:
        logging.error(f"VoteOptionItem with id {option_id} does not exist.")
        response['message'] = 'Tanlangan variant topilmadi.'
        response['status'] = False
        return response

    except Exception as err:
        logging.error(f"Unexpected error in user_vote: {err}")
        response['message'] = 'Noma’lum xatolik yuz berdi.'
        response['status'] = False
        return response


    
        
