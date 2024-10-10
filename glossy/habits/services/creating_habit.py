from django.shortcuts import get_object_or_404
from users.models import User
from habits.models import HabitTemplate, Habit

def create_habit_from_template(user_id, template_id):
    """
    Создать привычку для пользователя на основе шаблона.
    """
    # Получаем пользователя и шаблон привычки
    user = get_object_or_404(User, id=user_id)
    habit_template = get_object_or_404(HabitTemplate, id=template_id)
    
    # Создаем новую привычку на основе шаблона
    new_habit = Habit.objects.create(
        user=user,
        name=habit_template.name,
        description=habit_template.description,
      #  habit_group=habit_template.habit_group,
        made_from = habit_template.id,
        goal=habit_template.goal,
        habit_type=habit_template.habit_type,
        repeat_period=habit_template.repeat_period,
        icon=habit_template.icon,
        track_time=habit_template.track_time,
        due_dates=habit_template.due_dates,
    )
    
    return new_habit
