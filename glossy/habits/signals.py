from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HabitProgress
from .tasks import send_reminder_notification

@receiver(post_save, sender=HabitProgress)
def habit_progress_created(sender, instance, created, **kwargs):
    if created:
        # Push notification to make a text when performing a track point
        send_reminder_notification.apply_async((instance.user.id,), countdown=10)