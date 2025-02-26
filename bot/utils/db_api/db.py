from asgiref.sync import sync_to_async
from botapp.models import BotUser, BotUserChannel


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
def add_channel(user_id, channel):
    try:
        user = BotUser.objects.get(user_id=user_id)
        channel, created = BotUserChannel.objects.get_or_create(user=user, defaults={'channel': channel})
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