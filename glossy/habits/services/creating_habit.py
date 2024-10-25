from django.shortcuts import get_object_or_404
from users.models import User
from habits.models import HabitTemplate, Habit, RoutineTask, HabitTemplateTranslation


def create_habit_from_template(user_id, template_id, user_locale=""):
    """
    Создать привычку для пользователя на основе шаблона.
    """
    # Получаем пользователя и шаблон привычки
    user = get_object_or_404(User, id=user_id)
    habit_template = get_object_or_404(HabitTemplate, id=template_id)

    try:
        translation = habit_template.translations.get(language_code=user_locale)
        name = translation.name
        description = translation.description
    except HabitTemplateTranslation.DoesNotExist:
        # Если перевода на нужный язык нет, используем оригинальные поля
        name = habit_template.name
        description = habit_template.description

    new_habit_data = {
        "user": user,
        "name": name,
        "description": description,
        "habit_group": habit_template.habit_group,
        "made_from": habit_template,
        "goal": habit_template.goal,
        "habit_type": habit_template.habit_type,
        "repeat_period": habit_template.repeat_period,
        "icon": habit_template.icon,
        "track_time": habit_template.track_time,
        "due_dates": habit_template.due_dates,
    }

    # Создаем новую привычку на основе шаблона
    if habit_template.habit_type == "routine":
        # Создаем привычку с типом "routine" и задачами
        #!!!!!!!!!Сделай ТРАНЗАКЦИЮ
        new_habit_data["goal"] = len(habit_template.routine_tasks)
        new_habit = Habit.objects.create(**new_habit_data)
        # Добавляем связанные задачи (данные можно расширить для задания шаблонов задач)
        for task in habit_template.routine_tasks:
            RoutineTask.objects.create(habit=new_habit, name=task, is_done=False)
    else:
        # Обычная "regular" привычка
        new_habit = Habit.objects.create(**new_habit_data)
    return new_habit
