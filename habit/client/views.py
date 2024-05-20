from rest_framework import generics
from rest_framework import permissions

from users.models import User
from manage_hab.models import Habit, HabitProgress, HabitGroup
from .serializers import (
    HabitGroupSerializer,
    UserSerializer,
    HabitSerializer,
    HabitSerializerdates,
)


class CreateUser(generics.CreateAPIView):
    """
    Create user after firebase autroization
    """

    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete user profile
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HabitListCreateApiView(generics.ListCreateAPIView):
    """
    Get list of habits of current user, create new habit
    """

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        query_set = Habit.objects.filter(user=self.kwargs["pk"])
        return query_set


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete current users habit
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class Habitdates(generics.ListAPIView):
    """
    Read all users habit progress updates
    """

    serializer_class = HabitSerializerdates
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        query_set = HabitProgress.objects.values("update_time").filter(
            user=self.kwargs["pk"]
        )
        return query_set


class CurrentHabitdates(generics.ListAPIView):
    """
    Read current users habit progress updates
    """

    serializer_class = HabitSerializerdates
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        query_set = (
            HabitProgress.objects.values("update_time")
            .filter(user=self.kwargs["pk"])
            .filter(habit=self.kwargs["habit_id"])
        )
        return query_set


class HabitGroupListApiView(generics.ListAPIView):
    """
    Read all habit groups
    """

    queryset = HabitGroup.objects.all()
    serializer_class = HabitGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
