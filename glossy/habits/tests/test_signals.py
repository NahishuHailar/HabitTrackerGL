import pytest
from unittest.mock import patch
from django.contrib.auth import get_user_model
from habits.models import HabitProgress, Habit

User = get_user_model()

@pytest.mark.django_db
@patch('habits.signals.send_reminder_notification.apply_async')
def test_habit_progress_signal(mock_apply_async):
    user = User.objects.create_user(username="testuser", password="password123")

    habit = Habit.objects.create(name="Test Habit", user=user)

    habit_progress = HabitProgress.objects.create(user=user, habit=habit, current_value=5)
    
    # Проверяем, что функция apply_async была вызвана
    assert mock_apply_async.called
    
    # Проверяем, что задача отправлена с правильными аргументами и задержкой
    mock_apply_async.assert_called_with((user.id,), countdown=10)
