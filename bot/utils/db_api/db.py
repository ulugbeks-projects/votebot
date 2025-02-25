from asgiref.sync import sync_to_async
from botapp.models import BotUser


@sync_to_async
def get_or_create_user(user_id: str, first_name: str, last_name: str = None, username: str = None):
    user, created = BotUser.objects.get_or_create(
        user_id=user_id,
        defaults={'username': username, 'first_name': first_name, 'last_name': last_name}
    )
    return user, created