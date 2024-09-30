import pytest
from habits.models import Habit, HabitProgress, HabitHistory, HabitGroup, Icon  
from users.models import User

@pytest.mark.django_db
def test_habit_creation():
    user = User.objects.create_user(
        username="testuser", email="testuser@example.com", password="password123"
    )
    habit = Habit.objects.create(
        user=user, name="Test Habit", goal=10, current_value=5, status="active"
    )
    assert habit.name == "Test Habit"
    assert habit.user == user
    assert habit.goal == 10
    assert habit.current_value == 5
    assert habit.status == "active"


@pytest.mark.django_db
def test_routine_task_creation():
    user = User.objects.create_user(
        username="testuser", email="testuser@example.com", password="password123"
    )
    habit = Habit.objects.create(user=user, name="Test Routine Habit", goal=1)
    task = habit.routine_tasks.create(name="Test Task", is_done=False)
    
    assert task.name == "Test Task"
    assert task.is_done is False
    assert task.habit == habit

@pytest.mark.django_db
def test_habit_progress_creation():
    user = User.objects.create_user(
        username="testuser", email="testuser@example.com", password="password123"
    )
    habit = Habit.objects.create(user=user, name="Test Habit", goal=10)
    progress = HabitProgress.objects.create(
        habit=habit, user=user, current_value=5, current_goal=10
    )
    
    assert progress.habit == habit
    assert progress.user == user
    assert progress.current_value == 5
    assert progress.current_goal == 10

@pytest.mark.django_db
def test_habit_history_creation():
    user = User.objects.create_user(
        username="testuser", email="testuser@example.com", password="password123"
    )
    habit = Habit.objects.create(user=user, name="Test Habit", goal=10)
    history = HabitHistory.objects.create(habit=habit, user=user, date="2024-01-01", status="active")
    
    assert history.habit == habit
    assert history.user == user
    assert history.date == "2024-01-01"
    assert history.status == "active"


@pytest.mark.django_db
def test_habit_group_creation():
    group = HabitGroup.objects.create(name="Fitness", color="blue", product_id="fit001", paid=True)
    
    assert group.name == "Fitness"
    assert group.color == "blue"
    assert group.product_id == "fit001"
    assert group.paid is True


@pytest.mark.django_db
def test_icon_creation():
    group = HabitGroup.objects.create(name="Fitness", color="blue")
    icon = Icon.objects.create(name="Dumbbell", emoji_name="🏋️‍♂️", habit_group=group, paid=False)
    
    assert icon.name == "Dumbbell"
    assert icon.emoji_name == "🏋️‍♂️"
    assert icon.habit_group == group
    assert icon.paid is False