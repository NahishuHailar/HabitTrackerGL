from rest_framework import serializers
from users.models import User
from manage_hab.models import Habit, HabitGroup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "image", "email")


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class HabitSerializerdates(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("update_time",)


class HabitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitGroup()
        fields = ("name",)
