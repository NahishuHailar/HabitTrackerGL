from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from users.models import User
from manage_hab.models import Habbit, HabbitProgress, HabbitGroup
from .serializers import HabbitGroupSerializer, UserSerializer, HabbitSerializer, HabbitSerializerdates


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
    permission_classes = (permissions.IsAuthenticated, )


class HabbitListCreateApiView(generics.ListCreateAPIView):
    """
    Get list of habits of current user, create new habit
    """
    serializer_class = HabbitSerializer
    permission_classes = (permissions.IsAuthenticated, )    

    def get_queryset(self):
        query_set = Habbit.objects.filter(user=self.kwargs['pk'])
        return query_set



class HabbitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete current users habit
    """
    serializer_class = HabbitSerializer
    queryset = Habbit.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

class Habbitdates(generics.ListAPIView):
    """
    Read all users habit progress updates
    """
    serializer_class = HabbitSerializerdates
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        query_set = HabbitProgress.objects.values('update_time').filter(user=self.kwargs['pk'])
        return query_set
    

class CurrentHabbitdates(generics.ListAPIView):
    """
    Read current users habit progress updates
    """
    serializer_class = HabbitSerializerdates
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        query_set = HabbitProgress.objects.values('update_time').filter(user=self.kwargs['pk']).filter(habbit=self.kwargs['habbit_id'])
        return query_set
    

class HabbitGroupListApiView(generics.ListAPIView):
    """
    Read all habit groups
    """
    queryset = HabbitGroup.objects.all()
    serializer_class = HabbitGroupSerializer
    permission_classes = (permissions.IsAuthenticated, )