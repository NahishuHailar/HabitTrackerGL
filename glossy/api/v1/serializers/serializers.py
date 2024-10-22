from rest_framework import serializers
from users.models import User, UserAvatar, AvatarGroup
from habits.models import Habit, HabitGroup, HabitProgress, Icon, RoutineTask, HabitTemplate, LifeSpheres, TemplateBundles
from habits.services.creating_habit import create_habit_from_template


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
    # routine_tasks = serializers.ListField(
    #     child=serializers.DictField(child=serializers.BooleanField()), required=False
    # )

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
                {task.name: task.is_done} for task in instance.routine_tasks.all()
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
        if "routine_tasks" not in validated_data.keys():
            habit = Habit.objects.create(**validated_data)
            return habit

        routine_tasks_data = validated_data.pop("routine_tasks", None)
        
        validated_data['habit_type'], validated_data['repeat_period'] = "routine", "day"
        validated_data['goal'], validated_data['current_value'] = 0, 0
        if routine_tasks_data:
            goal, current_value = len(routine_tasks_data), 0
            for task_data in routine_tasks_data:
                if list(task_data.values())[0]:
                    current_value += 1
            validated_data['goal'], validated_data['current_value'] = goal, current_value       
        
        habit = Habit.objects.create(**validated_data)
            
        # Если это привычка типа "routine", создаем задачи
        if routine_tasks_data:

            for task_data in routine_tasks_data:
                # task_data — это словарь, где ключ — название задачи, а значение — её статус (True/False)
                for task_name, is_done in task_data.items():
                    RoutineTask.objects.create(habit=habit, name=task_name, is_done=is_done)


        return habit

    def update(self, instance, validated_data):
        routine_tasks_data = validated_data.pop("routine_tasks", None)
        habit_type = validated_data.get("habit_type", None)
        if habit_type and habit_type == "regular":
            instance = super().update(instance, validated_data)
            return instance

        validated_data['goal'], validated_data['current_value'] = 0, 0
        if routine_tasks_data:
            goal, current_value = len(routine_tasks_data), 0
            for task_data in routine_tasks_data:
                if list(task_data.values())[0]:
                    current_value += 1
            
            request = self.context.get('request')
            if instance.current_value is None:
                instance.current_value = 0
            if int(instance.current_value) < current_value and request.method == 'PATCH':
                HabitProgress.objects.create(
                habit=instance,
                user_id=request.user.id,
                current_goal=goal,
                current_value=current_value
            )   

            validated_data['goal'], validated_data['current_value'] = goal, current_value
        # Обновляем задачи рутины, если это привычка типа "routine"
        instance.routine_tasks.all().delete()  # Удаляем старые задачи
        if routine_tasks_data:
            for task_data in routine_tasks_data:
                for task_name, is_done in task_data.items():
                    RoutineTask.objects.create(habit=instance, name=task_name, is_done=is_done)            
        instance = super().update(instance, validated_data)
        validated_data["routine_tasks"] = routine_tasks_data
        return instance
    

class RoutineTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineTask
        fields = ['id', 'name', 'is_done']


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

class CreateHabitFromTemplateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    template_id = serializers.IntegerField()

    def create(self, validated_data):
        # Вызываем сервис для создания привычки
        new_habit = create_habit_from_template(
            user_id=validated_data['user_id'], 
            template_id=validated_data['template_id']
        )
        return new_habit
    

class HabitTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitTemplate
        fields = '__all__'    
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Отображение группы привычек по имени
        if instance.habit_group:
            rep["habit_group"] = instance.habit_group.name
        
        # Отображение задач рутины для привычки типа "routine"
        if instance.habit_type == "routine":
            rep["routine_tasks"] = [
                {task.name: task.is_done} for task in instance.routine_tasks.all()
            ]
        return rep

    def to_internal_value(self, data):
        data_copy = data.copy()

        # Обработка habit_group по имени
        habit_group_value = data_copy.get("habit_group")
        if habit_group_value:
            try:
            # Если значение — это UUID (ID группы), используем его напрямую
                if isinstance(habit_group_value, (int, str)):
                    if HabitGroup.objects.filter(id=habit_group_value).exists():
                        data_copy["habit_group"] = habit_group_value
                    else:
                        # Если это не ID, попробуем найти по имени
                        habit_group = HabitGroup.objects.get(name=habit_group_value)
                        data_copy["habit_group"] = habit_group.id
                else:
                    raise serializers.ValidationError("Invalid habit group format.")
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
    

class LifeSpheresSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeSpheres
        fields = '__all__'    
        

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Отображение группы привычек по имени
        if instance.habit_group:
            rep["habit_group"] = instance.habit_group.name
        
        return rep

    def to_internal_value(self, data):
        data_copy = data.copy()

        # Обработка habit_group по имени
        habit_group_value = data_copy.get("habit_group")
        if habit_group_value:
            try:
            # Если значение — это UUID (ID группы), используем его напрямую                
                if habit_group_value.isdigit():
                    if HabitGroup.objects.filter(id=habit_group_value).exists():
                        data_copy["habit_group"] = habit_group_value
                    else:
                        raise serializers.ValidationError("Habit group does not exist.")     
                else:
                    # Если это не ID, попробуем найти по имени
                    habit_group = HabitGroup.objects.get(name=habit_group_value)
                    data_copy["habit_group"] = habit_group.id
            except HabitGroup.DoesNotExist:
                raise serializers.ValidationError("Habit group does not exist.")
            
        # Преобразование и проверка данных с помощью родительского метода
        validated_data = super().to_internal_value(data_copy)

        return validated_data    

class TemplateBundlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateBundles
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # Отображение LifeSpheres по имени
        if instance.life_spheres:
            rep["life_spheres"] = instance.life_spheres.name
        
        # Отображение родительского TemplateBundles по имени

        if instance.parent_bundle:
            rep["parent_bundle"] = instance.parent_bundle.name
            
        return rep

    def to_internal_value(self, data):
        data_copy = data.copy()

        # Обработка life_spheres по имени
        life_spheres_value = data_copy.get("life_spheres")
        if life_spheres_value:
            try:
                # Если значение — ID сферы жизни используем его напрямую
                if life_spheres_value.isdigit():
                    if LifeSpheres.objects.filter(id=life_spheres_value).exists():
                        data_copy["life_spheres"] = life_spheres_value
                        # Если это не ID, попробуем найти по имени
                else:          
                    life_spheres = LifeSpheres.objects.get(name=life_spheres_value)
                    data_copy["life_spheres"] = life_spheres.id
            except HabitGroup.DoesNotExist:
                raise serializers.ValidationError("Life_spheres does not exist.")

        # Обработка parent_bundle по имени
        parent_bundle_value = data_copy.get("parent_bundle")
        if parent_bundle_value:
            try:
            # Если значение — ID parent_bundle используем его напрямую
                if parent_bundle_value.isdigit():
                    if TemplateBundles.objects.filter(id=parent_bundle_value).exists():
                        data_copy["parent_bundle"] = parent_bundle_value
                else:
                    # Если это не ID, попробуем найти по имени
                    parent_bundle = TemplateBundles.objects.get(name=parent_bundle_value)
                    data_copy["parent_bundle"] = parent_bundle.id
               
            except HabitGroup.DoesNotExist:
                raise serializers.ValidationError("Parent_bundle - TemplateBundles does not exist.")


        # Преобразование и проверка данных с помощью родительского метода
        validated_data = super().to_internal_value(data_copy)

        return validated_data        