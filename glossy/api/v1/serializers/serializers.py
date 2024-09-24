from rest_framework import serializers
from users.models import User, UserAvatar, AvatarGroup
from habits.models import Habit, HabitGroup, HabitProgress, Icon, RoutineTask


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "firebase_key", "auth_type", "image"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        ref_name = "CustomUserModelSerialize"

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        if instance.avatar:
            rep["avatar"] = instance.avatar.title
        return rep

    def to_internal_value(self, data):
        data_copy = data.copy()
        user_avatar_title = data_copy.get("avatar", None)
        if user_avatar_title:
            try:
                user_avatar_id = UserAvatar.objects.get(title=user_avatar_title).id
                data_copy["avatar"] = user_avatar_id
            except UserAvatar.DoesNotExist:
                raise serializers.ValidationError("UserAvatar does not exist.")
        return super().to_internal_value(data_copy)


class HabitSerializer(serializers.ModelSerializer):
    routine_tasks = serializers.ListSerializer(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    class Meta:
        model = Habit
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Отображение группы привычек по имени
        if instance.habit_group:
            rep["habit_group"] = instance.habit_group.name
        
        # Отображение задач рутины для привычки типа "routine"
        if instance.habit_type == "routine":
            rep["routine_tasks"] = [
                task.name for task in instance.routine_tasks.all()
            ]
        return rep

    def to_internal_value(self, data):
        data_copy = data.copy()

        # Обработка habit_group по имени
        habit_group_name = data_copy.get("habit_group")
        if habit_group_name:
            try:
                habit_group_id = HabitGroup.objects.get(name=habit_group_name).id
                data_copy["habit_group"] = habit_group_id
            except HabitGroup.DoesNotExist:
                raise serializers.ValidationError("Habit group does not exist.")

        # Обработка задач для рутины
        routine_tasks_data = data_copy.pop("routine_tasks", None)
        
        # Преобразование и проверка данных с помощью родительского метода
        validated_data = super().to_internal_value(data_copy)

        # Добавление задач рутины, если они присутствуют
        if routine_tasks_data:
            validated_data["routine_tasks"] = routine_tasks_data

        return validated_data

    def create(self, validated_data):
        routine_tasks_data = validated_data.pop("routine_tasks", None)
        habit = Habit.objects.create(**validated_data)

        # Если это привычка типа "routine", создаем задачи
        if habit.habit_type == "routine" and routine_tasks_data:
            for task_name in routine_tasks_data:
                RoutineTask.objects.create(habit=habit, name=task_name)

        return habit

    def update(self, instance, validated_data):
        routine_tasks_data = validated_data.pop("routine_tasks", None)
        instance = super().update(instance, validated_data)

        # Обновляем задачи рутины, если это привычка типа "routine"
        if instance.habit_type == "routine":
            instance.routine_tasks.all().delete()  # Удаляем старые задачи
            if routine_tasks_data:
                for task_name in routine_tasks_data:
                    RoutineTask.objects.create(habit=instance, name=task_name)

        return instance
    

class RoutineTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineTask
        fields = ['id', 'name']


class HabitDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitProgress
        fields = "__all__"


class HabitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitGroup
        fields = "__all__"


class AvatarGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarGroup
        fields = "__all__"


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(AvatarSerializer, self).to_representation(instance)
        if instance.avatar_group:
            rep["avatar_group"] = instance.avatar_group.name
        return rep


class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(IconSerializer, self).to_representation(instance)
        rep["habit_group"] = instance.habit_group.name
        return rep
