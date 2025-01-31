from rest_framework import serializers
from users.models import User, UserAvatar, AvatarGroup, UserTrial
from habits.models import (
    Habit,
    HabitGroup,
    HabitProgress,
    Icon,
    RoutineTask,
    HabitTemplate,
    LifeSpheres,
    TemplateBundles,
    TemplateBundlesTranslation,
)
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

        validated_data["habit_type"], validated_data["repeat_period"] = "routine", "day"
        validated_data["goal"], validated_data["current_value"] = 0, 0
        if routine_tasks_data:
            goal, current_value = len(routine_tasks_data), 0
            for task_data in routine_tasks_data:
                if list(task_data.values())[0]:
                    current_value += 1
            validated_data["goal"], validated_data["current_value"] = (
                goal,
                current_value,
            )

        habit = Habit.objects.create(**validated_data)

        # Если это привычка типа "routine", создаем задачи
        if routine_tasks_data:

            for task_data in routine_tasks_data:
                # task_data — это словарь, где ключ — название задачи, а значение — её статус (True/False)
                for task_name, is_done in task_data.items():
                    RoutineTask.objects.create(
                        habit=habit, name=task_name, is_done=is_done
                    )

        return habit

    def update(self, instance, validated_data):
        routine_tasks_data = validated_data.pop("routine_tasks", None)
        habit_type = validated_data.get("habit_type", None)
        if habit_type and habit_type == "regular":
            instance = super().update(instance, validated_data)
            return instance

        validated_data["goal"], validated_data["current_value"] = 0, 0
        if routine_tasks_data:
            goal, current_value = len(routine_tasks_data), 0
            for task_data in routine_tasks_data:
                if list(task_data.values())[0]:
                    current_value += 1

            request = self.context.get("request")
            if instance.current_value is None:
                instance.current_value = 0
            if (
                int(instance.current_value) < current_value
                and request.method == "PATCH"
            ):
                HabitProgress.objects.create(
                    habit=instance,
                    user_id=request.user.id,
                    current_goal=goal,
                    current_value=current_value,
                )

            validated_data["goal"], validated_data["current_value"] = (
                goal,
                current_value,
            )
        # Обновляем задачи рутины, если это привычка типа "routine"
        instance.routine_tasks.all().delete()  # Удаляем старые задачи
        if routine_tasks_data:
            for task_data in routine_tasks_data:
                for task_name, is_done in task_data.items():
                    RoutineTask.objects.create(
                        habit=instance, name=task_name, is_done=is_done
                    )
        instance = super().update(instance, validated_data)
        validated_data["routine_tasks"] = routine_tasks_data
        return instance


class RoutineTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineTask
        fields = ["id", "name", "is_done"]


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
    user_locale = serializers.CharField(required=False, allow_blank=True, default="en")

    def create(self, validated_data):
        # Вызываем сервис для создания привычки
        new_habit = create_habit_from_template(
            user_id=validated_data["user_id"],
            template_id=validated_data["template_id"],
            user_locale=validated_data.get("user_locale", "en"),
        )
        return new_habit


class HabitTemplateListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = HabitTemplate
        fields = [
            "id",
            "name",
            "short_description",
            "icon",
            "habit_group",
            "text_is_ai_generated",
            "paid",
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Отображение группы привычек по имени
        if instance.habit_group:
            rep["habit_group"] = instance.habit_group.name

        return rep

    def get_name(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.name if translation else obj.name

    def get_short_description(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.description if translation else obj.short_description


class HabitTemplateDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = HabitTemplate
        fields = "__all__"

    def get_name(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.name if translation else obj.name

    def get_description(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.description if translation else obj.description

    def get_short_description(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.short_description if translation else obj.short_description

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
        fields = "__all__"

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


from rest_framework import serializers


class TemplateBundlesTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateBundlesTranslation
        fields = ["language_code", "name", "description"]


class TemplateBundlesSerializer(serializers.ModelSerializer):
    templates = serializers.PrimaryKeyRelatedField(
        many=True, queryset=HabitTemplate.objects.all()
    )
    sub_bundles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TemplateBundles.objects.all()
    )
    life_spheres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=LifeSpheres.objects.all()
    )
    translations = TemplateBundlesTranslationSerializer(many=True, required=False)

    class Meta:
        model = TemplateBundles
        fields = [
            "id",
            "name",
            "description",
            "templates",
            "sub_bundles",
            "life_spheres",
            "translations",
        ]

    def validate_sub_bundles(self, sub_bundles):
        """
        Проверка на циклические зависимости в поднаборах.
        """
        if any(bundle.has_cyclic_dependency({self.instance}) for bundle in sub_bundles):
            raise serializers.ValidationError("Cyclic dependency detected.")
        return sub_bundles

    def get_name(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.name if translation else obj.name

    def get_description(self, obj):
        user_locale = self.context.get("user_locale", "en")
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.description if translation else obj.description


class TemplateBundlesListSerializer(serializers.ModelSerializer):
    templates = serializers.SerializerMethodField()
    sub_bundles = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = TemplateBundles
        fields = ['id', 'name', 'description', 'templates', 'sub_bundles']

    def get_templates(self, obj):
        """
        Возвращает список имен шаблонов с учётом локализации.
        """
        user_locale = self.context.get('user_locale', 'en')
        return [
            template.translations.filter(language_code=user_locale).first().name 
            if template.translations.filter(language_code=user_locale).exists() 
            else template.name
            for template in obj.templates.all()
        ]

    def get_sub_bundles(self, obj):
        """
        Возвращает список имен поднаборов с учётом локализации.
        """
        user_locale = self.context.get('user_locale', 'en')
        return [
            sub_bundle.translations.filter(language_code=user_locale).first().name 
            if sub_bundle.translations.filter(language_code=user_locale).exists() 
            else sub_bundle.name
            for sub_bundle in obj.sub_bundles.all()
        ]

    def get_name(self, obj):
        """
        Возвращает локализованное имя или стандартное имя, если перевода нет.
        """
        user_locale = self.context.get('user_locale', 'en')
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.name if translation else obj.name

    def get_description(self, obj):
        """
        Возвращает локализованное описание или стандартное описание, если перевода нет.
        """
        user_locale = self.context.get('user_locale', 'en')
        translation = obj.translations.filter(language_code=user_locale).first()
        return translation.description if translation else obj.description
   


class UserTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrial
        fields = ['first_trial_date', 'second_trial_date']