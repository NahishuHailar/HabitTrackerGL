import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from firebase_admin import messaging

User = get_user_model()

logger = logging.getLogger("celery_tasks")


@shared_task
def send_reminder_notification(user_id):
    try:
        user = User.objects.get(id=user_id)

        # Making push notification
        message = messaging.Message(
            notification=messaging.Notification(
                title="Напоминание",
                body="Не забудьте заполнить данные о контексте выполнения вашей привычки!",
            ),
            token=user.fcm_key,
        )

        # Sending notification by FCM
        response = messaging.send(message)

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")
    except Exception as e:
        logger.exception(
            f"An error occurred while sending notification to user {user_id}: {str(e)}"
        )
