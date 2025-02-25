from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'user_id', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'username', 'user_id')
    list_filter = ('created_at', 'updated_at')



admin.site.register(BotUser, BotUserAdmin)
