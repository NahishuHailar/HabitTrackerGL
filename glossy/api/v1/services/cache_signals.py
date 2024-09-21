"""
Deleting the cache when updating related models
"""

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse

from habits.models import Icon, HabitGroup
from users.models import UserAvatar, AvatarGroup


def clear_view_cache(view_name, args=None):
    """
    Clear the cache for a specific view by its name.
    """
    url = reverse(view_name, args=args)
    cache_key = f"views.decorators.cache.cache_page.{url}"
    cache.delete(cache_key)


@receiver(post_save, sender=HabitGroup)
@receiver(post_delete, sender=HabitGroup)
def clear_habit_group_cache(sender, **kwargs):
    clear_view_cache("avatargroup_list")


@receiver(post_save, sender=Icon)
@receiver(post_delete, sender=Icon)
def clear_icon_cache(sender, **kwargs):
    clear_view_cache("icon_list")


@receiver(post_save, sender=UserAvatar)
@receiver(post_delete, sender=UserAvatar)
def clear_avatar_cache(sender, **kwargs):
    clear_view_cache("avatar_list")



@receiver(post_save, sender=AvatarGroup)
@receiver(post_delete, sender=AvatarGroup)
def clear_avatar_group_cache(sender, **kwargs):
    clear_view_cache("avatar_list")