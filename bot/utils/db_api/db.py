from asgiref.sync import sync_to_async
from botapp.models import BotUser, BotUserChannel


@sync_to_async
def get_or_create_user(user_id: str, first_name: str, last_name: str|None, username: str|None):
    user, created = BotUser.objects.get_or_create(user_id=user_id,
                                                  defaults={'first_name': first_name,
                                                            'last_name': last_name,
                                                            'username': username})
    return user, created



@sync_to_async
def add_channel(channel, user_id, is_admin=False):
    try:
        user = BotUser.objects.get(user_id=user_id)
        channel, created = BotUserChannel.objects.get_or_create(
            channel=channel,
            defaults={'user': user, 'is_admin': is_admin}
        )
        return channel, created
    except BotUser.DoesNotExist:
        return None, False
    
    except BotUserChannel.DoesNotExist:
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
    
    except BotUserChannel.DoesNotExist:
        return None
    
    except Exception as e:
        return None
    
    
    