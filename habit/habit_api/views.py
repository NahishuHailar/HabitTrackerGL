import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from users.models import User, UserAvatar, AvatarGroup
from manage_hab.models import Habit, HabitProgress, HabitGroup, Icon
from .serializers import (
    HabitGroupSerializer,
    UserSerializer,
    HabitSerializer,
    HabitDatesSerializer,
    AvatarSerializer,
    IconSerializer,
    AvatarGroupSerializer,
)
from .utils import get_user_cred
from manage_hab.services.habit_counters import reset_habits_counters
from manage_hab.services.habit_calendar.get_calendar import (
    get_progress_calendar, get_common_progress_calendar
)

logger = logging.getLogger(__name__)


class GetUserAPIView(APIView):
    """
    Get current user. The user is created during the Firebase
    authorization process (users.authentication).
    Credential data of the current user is located
    in the Firebase token (used get_user_cred).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_key = get_user_cred(request)
        current_user = User.objects.filter(firebase_key=filter_key).first()
        if current_user:
            return Response(UserSerializer(current_user).data)
        return Response({"detail": "User not found"}, status=404)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete user profile
    """

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        self.kwargs['pk'] = self.kwargs['user_id']
        query_set = User.objects.filter(pk=self.kwargs["pk"])
        return query_set


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """
    Get list of habits of current user, create new user's habit
    """

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if local_time := self.request.META.get('HTTP_LOCAL_TIME', None):   
            reset_habits_counters(self.kwargs["user_id"], local_time)    
        return Habit.active.filter(user=self.kwargs["user_id"])


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete current users habit
    """

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #Setting the pk for the current object
        self.kwargs["pk"] = self.kwargs["habit_id"]
        query_set = (
            Habit.objects.filter(pk=self.kwargs["habit_id"], user_id=self.kwargs["user_id"])
            .select_related("habit_group")
        )
        return query_set
    
    def patch(self, request, *args, **kwargs):
        """
        When changing the current value of a habit, we create an entry in HabitProgress
        """
        # Getting the current habit
        habit = self.get_object()    
        # Checking if the current_value has changed
        new_current_value = request.data.get("current_value")
        if new_current_value and habit.current_value != int(new_current_value):
        # Creating a new progress record
            HabitProgress.objects.create(
                habit=habit,
                user_id=self.kwargs["user_id"],
                current_goal=habit.goal,
                current_due_dates=habit.due_dates,
                current_value=new_current_value
            )         
        return super().patch(request, *args, **kwargs)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Changing the status to "deleted" instead of deleting
        instance.status = "deleted"
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class HabitDatesListAPIView(generics.ListAPIView):
    """
    Read all current user habit progress updates
    """

    serializer_class = HabitDatesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return HabitProgress.objects.filter(
            user_id=self.kwargs["user_id"]
        ).order_by("habit")


class CurrentHabitDatesListAPIView(generics.ListAPIView):
    """
    Read current users habit progress updates
    """

    serializer_class = HabitDatesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        return HabitProgress.objects.filter(
            user_id=self.kwargs["user_id"], habit_id=self.kwargs["habit_id"]
        )
        

@method_decorator(cache_page(30), name='dispatch')
class HabitGroupListAPIView(generics.ListAPIView):
    """
    Read all habit groups
    """

    queryset = HabitGroup.objects.all()
    serializer_class = HabitGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name='dispatch')
class AvatarListAPIView(generics.ListAPIView):
    """
    Get list avatars urls
    """

    queryset = UserAvatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name='dispatch')
class IconListListAPIView(generics.ListAPIView):
    """
    Get list of icons.
    """

    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name='dispatch')
class AvatarGroupListAPIView(generics.ListAPIView):
    """
    Read all habit groups
    """

    queryset = AvatarGroup.objects.all()
    serializer_class = AvatarGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)



class HabitProgressAPIView(APIView):
    """
    Get progress list of current habit. For a current habit calendar.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, habit_id):
        pagination = int(request.query_params.get('pagination', 1)) 
        progress_calendar = get_progress_calendar(
            user_id=user_id, 
            habit_id=habit_id, 
            pagination=pagination
        )
        return Response(progress_calendar)


class CommonHabitProgressAPIView(APIView):
    """
    Get common progress list. Overall result of habit execution.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, requet, user_id):
        common_progress_calendar = get_common_progress_calendar(user_id=user_id)
        return Response(common_progress_calendar)
