from rest_framework import serializers
from users.models import User
from manage_hab.models import Habit, HabitGroup, HabitProgress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "image", "email", "auth_type")
        ref_name = 'CustomUserModelSerialize'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitProgress
        fields = "__all__"


class HabitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitGroup()
        fields = ("name",)
