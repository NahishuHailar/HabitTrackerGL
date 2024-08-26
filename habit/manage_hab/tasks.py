from celery import shared_task
from django.contrib.auth import get_user_model
from firebase_admin import messaging

User = get_user_model()

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
            token=user.fcm_key,  # Предполагается, что у пользователя есть поле для хранения токена устройства
        )

        # Sending notification by FCM
        response = messaging.send(message)

    except User.DoesNotExist:
        print(f'User with id {user_id} does not exist')