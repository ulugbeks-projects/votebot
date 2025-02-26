from django.contrib import admin
from .models import (
    BotUser, BotUserChannel, VoteOptionItem, VoteOption, 
    VotePost, Vote
)


# Inline for displaying user channel in the BotUser admin page
class BotUserChannelInline(admin.TabularInline):
    model = BotUserChannel
    extra = 1  # Allows adding new channel entry inline


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "username", "language_code", "created_at")
    search_fields = ("user_id", "first_name", "last_name", "username")
    list_filter = ("language_code", "created_at")
    inlines = [BotUserChannelInline]  # Display related channels inline


@admin.register(BotUserChannel)
class BotUserChannelAdmin(admin.ModelAdmin):
    list_display = ("user", "channel", "is_admin", "created_at")
    search_fields = ("user__first_name", "user__last_name", "channel")
    list_filter = ("is_admin",)


# Inline for displaying vote items inside VoteOption admin
class VoteOptionItemInline(admin.TabularInline):
    model = VoteOption.items.through  # ManyToMany intermediate table
    extra = 1


@admin.register(VoteOptionItem)
class VoteOptionItemAdmin(admin.ModelAdmin):
    list_display = ("title", "vote_count", "created_at")
    search_fields = ("title",)
    list_filter = ("created_at",)


@admin.register(VoteOption)
class VoteOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    inlines = [VoteOptionItemInline]  # Display vote items inline


# Inline for displaying votes inside VotePost admin
class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1


@admin.register(VotePost)
class VotePostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "media_type", "caption", "created_at")
    search_fields = ("caption", "user__first_name", "user__last_name")
    list_filter = ("media_type", "created_at")
    inlines = [VoteInline]  # Display votes inline


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "option", "created_at")
    search_fields = ("user__first_name", "post__caption", "option__title")
    list_filter = ("created_at",)
