# # tests/unit/test_habit_counters.py
# import pytest
# from unittest import mock
# from datetime import datetime, timedelta
# from habits.models import Habit
# from api.v1.services.habit_counters import reset_habits_counters

# @pytest.fixture
# def user(db, django_user_model):
#     """
#     Создаём фикстуру пользователя для тестов.
#     """
#     return django_user_model.objects.create_user(username="testuser", password="password123")

# @pytest.fixture
# def habit_factory(user):
#     """
#     Фикстура для создания различных привычек.
#     """
#     def create_habit(repeat_period, update_time):
#         return Habit.objects.create(
#             user=user,
#             name=f"Test Habit {repeat_period}",
#             repeat_period=repeat_period,
#             update_time=update_time,
#             current_value=5  # Например, прогресс в привычке
#         )
#     return create_habit

# @pytest.mark.django_db
# @mock.patch('api.v1.services.habit_counters.reset_current_value')
# def test_daily_reset(mock_reset_current_value, user, habit_factory):
#     """
#     Тестируем сброс ежедневных привычек.
#     """
#     # Создаём привычку с периодом "день"
#     habit = habit_factory("day", datetime.now() - timedelta(days=2))  # Привычка была обновлена 2 дня назад

#     # Вызываем функцию сброса
#     reset_habits_counters(user.id, (datetime.now()).isoformat())

#     # Проверяем, что сброс был вызван
#     mock_reset_current_value.assert_called_once_with(habit)


# @pytest.mark.django_db
# @mock.patch('api.v1.services.habit_counters.reset_current_value')
# def test_weekly_reset(mock_reset_current_value, user, habit_factory):
#     """
#     Тестируем сброс еженедельных привычек.
#     """
#     # Создаём привычку с периодом "неделя"
#     habit = habit_factory("week", datetime.now() - timedelta(weeks=2))  # Привычка была обновлена 2 недели назад

#     # Вызываем функцию сброса
#     reset_habits_counters(user.id, (datetime.now()).isoformat())

#     # Проверяем, что сброс был вызван
#     mock_reset_current_value.assert_called_once_with(habit)


# @pytest.mark.django_db
# @mock.patch('api.v1.services.habit_counters.reset_current_value')
# def test_monthly_reset(mock_reset_current_value, user, habit_factory):
#     """
#     Тестируем сброс ежемесячных привычек.
#     """
#     # Создаём привычку с периодом "месяц"
#     habit = habit_factory("month", datetime.now().replace(month=(datetime.now().month - 2) % 12))

#     # Вызываем функцию сброса
#     reset_habits_counters(user.id, (datetime.now()).isoformat())

#     # Проверяем, что сброс был вызван
#     mock_reset_current_value.assert_called_once_with(habit)


# @pytest.mark.django_db
# @mock.patch('api.v1.services.habit_counters.reset_current_value')
# def test_annual_reset(mock_reset_current_value, user, habit_factory):
#     """
#     Тестируем сброс ежегодных привычек.
#     """
#     # Создаём привычку с периодом "год"
#     habit = habit_factory("year", datetime.now().replace(year=(datetime.now().year - 2)))

#     # Вызываем функцию сброса
#     reset_habits_counters(user.id, (datetime.now()).isoformat())

#     # Проверяем, что сброс был вызван
#     mock_reset_current_value.assert_called_once_with(habit)
