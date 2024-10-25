import logging

from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.utils.decorators import method_decorator

from users.models import User, UserAvatar, AvatarGroup, UserTrial
from habits.models import (
    Habit,
    HabitProgress,
    HabitGroup,
    Icon,
    HabitTemplate,
    LifeSpheres,
    TemplateBundles,
)
from api.v1.serializers.serializers import (
    HabitGroupSerializer,
    UserSerializer,
    HabitSerializer,
    HabitDatesSerializer,
    AvatarSerializer,
    IconSerializer,
    AvatarGroupSerializer,
    CreateHabitFromTemplateSerializer,
    HabitTemplateListSerializer,
    HabitTemplateDetailSerializer,
    LifeSpheresSerializer,
    TemplateBundlesSerializer,
    UserTrialSerializer,
)
from users.auth.user_cred import get_user_cred
from api.v1.services.habit_counters import reset_habits_counters
from api.v1.services.calendars.get_calendar import (
    get_progress_calendar,
    get_common_progress_calendar,
)
from api.v1.services.old_calendars.get_old_calendar import (
    get_old_common_progress_calendar,
    get_old_progress_calendar,
)
from api.v1.services.update_habit_progress.routine_progress import check_input_progrees

from habits.services.creating_habit import create_habit_from_template

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
        self.kwargs["pk"] = self.kwargs["user_id"]
        query_set = User.objects.filter(pk=self.kwargs["pk"])
        return query_set


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """
    Get list of habits of current user, create new user's habit
    """

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if local_time := self.request.META.get("HTTP_LOCAL_TIME", None):
            reset_habits_counters(self.kwargs["user_id"], local_time)
        return Habit.active.filter(user=self.kwargs["user_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, update, delete current users habit
    """

    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Setting the pk for the current object
        self.kwargs["pk"] = self.kwargs["habit_id"]
        query_set = Habit.objects.filter(
            pk=self.kwargs["habit_id"], user_id=self.kwargs["user_id"]
        ).select_related("habit_group")
        return query_set

    def patch(self, request, *args, **kwargs):
        """
        When changing the current value of a habit, we create an entry in HabitProgress
        """
        # Getting the current habit
        habit = self.get_object()

        # Checking if the current_value has changed for regular habit
        new_current_value = request.data.get("current_value")
        if new_current_value and habit.current_value != int(new_current_value):
            # Creating a new progress record for regular habit
            HabitProgress.objects.create(
                habit=habit,
                user_id=self.kwargs["user_id"],
                current_goal=habit.goal,
                current_due_dates=habit.due_dates,
                current_value=new_current_value,
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
        return HabitProgress.objects.filter(user_id=self.kwargs["user_id"]).order_by(
            "habit"
        )


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


@method_decorator(cache_page(30), name="dispatch")
class HabitGroupListAPIView(generics.ListAPIView):
    """
    Read all habit groups
    """

    queryset = HabitGroup.objects.all()
    serializer_class = HabitGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name="dispatch")
class AvatarListAPIView(generics.ListAPIView):
    """
    Get list avatars urls
    """

    queryset = UserAvatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name="dispatch")
class IconListListAPIView(generics.ListAPIView):
    """
    Get list of icons.
    """

    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    permission_classes = (permissions.IsAuthenticated,)


@method_decorator(cache_page(30), name="dispatch")
class AvatarGroupListAPIView(generics.ListAPIView):
    """
    Read all habit groups
    """

    queryset = AvatarGroup.objects.all()
    serializer_class = AvatarGroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class HabitProgressPagAPIView(APIView):
    """
    Get progress list of current habit. For a current habit calendar.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, habit_id):
        pagination = int(request.query_params.get("pagination", 0))
        progress_calendar, last_page, out_of_range = get_progress_calendar(
            user_id=user_id, habit_id=habit_id, pagination=pagination
        )
        result = {}
        result["pagination"] = {"last_page": last_page, "out_of_range": out_of_range}
        result["data"] = progress_calendar
        return Response(result)


class CommonHabitProgressPagAPIView(APIView):
    """
    Get common progress list. Overall result of habit execution.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id):
        pagination = int(request.query_params.get("pagination", 0))
        common_progress_calendar, last_page, out_of_range = (
            get_common_progress_calendar(user_id=user_id, pagination=pagination)
        )

        result = {}
        result["pagination"] = {"last_page": last_page, "out_of_range": out_of_range}
        result["data"] = common_progress_calendar
        return Response(result)


class HabitProgressAPIView(APIView):
    """
    Get progress list of current habit. For a current habit calendar.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id, habit_id):
        progress_calendar = get_old_progress_calendar(
            user_id=user_id,
            habit_id=habit_id,
        )
        return Response(progress_calendar)


class CommonHabitProgressAPIView(APIView):
    """
    Get common progress list. Overall result of habit execution.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id):
        common_progress_calendar = get_old_common_progress_calendar(user_id=user_id)
        return Response(common_progress_calendar)


class HabitTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с шаблонами привычек и создания привычек на основе шаблонов.
    """

    queryset = HabitTemplate.objects.all()

    # Выбор сериализаторов в зависимости от типа запроса (список или детально)
    def get_serializer_class(self):
        if self.action == "list":
            return HabitTemplateListSerializer
        return HabitTemplateDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Получаем user_locale из параметров запроса или используем 'en' по умолчанию
        user_locale = self.request.query_params.get("user_locale", "en")
        context["user_locale"] = user_locale
        return context

    @action(detail=False, methods=["post"], url_path="create-habit-from-template")
    def create_habit_from_template(self, request):
        """
        Создать привычку на основе шаблона.
        """
        serializer = CreateHabitFromTemplateSerializer(data=request.data)
        if serializer.is_valid():
            new_habit = serializer.save()
            return Response(
                {
                    "habit_id": new_habit.id,
                    "habit_name": new_habit.name,
                    "habit_group": new_habit.habit_group.name,
                    "description": new_habit.description,
                    "goal": new_habit.goal,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LifeSpheresViewSet(viewsets.ModelViewSet):
    queryset = LifeSpheres.objects.all()
    serializer_class = LifeSpheresSerializer


class TemplateBundlesViewSet(viewsets.ModelViewSet):
    queryset = TemplateBundles.objects.all()
    serializer_class = TemplateBundlesSerializer

    @action(detail=True, methods=["post"], url_path="create-habits")
    def create_habits(self, request, pk=None):
        """
        Рекурсивно создаёт привычки из набора шаблонов и его поднаборов.
        """
        bundle = self.get_object()
        user_id = request.data.get("user_id")
        user_locale = request.data.get("user_locale", "en")

        if not user_id:
            return Response(
                {"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        created_habits = self._create_habits_from_bundle(bundle, user_id, user_locale)
        return Response(created_habits, status=status.HTTP_201_CREATED)

    def _create_habits_from_bundle(self, bundle, user_id, user_locale):
        created_habits = []
        for template in bundle.templates.all():
            habit = create_habit_from_template(
                user_id=user_id, template_id=template.id, user_locale=user_locale
            )
            created_habits.append({"habit_id": habit.id, "name": habit.name})

        # Рекурсивно создаём привычки из поднаборов
        for sub_bundle in bundle.sub_bundles.all():
            created_habits.extend(
                self._create_habits_from_bundle(sub_bundle, user_id, user_locale)
            )
        return created_habits


class UserTrialViewSet(viewsets.ViewSet):
    def list(self, request):
        # Получаем или создаем запись пробного периода для пользователя
        trial, created = UserTrial.objects.get_or_create(user=request.user)
        serializer = UserTrialSerializer(trial)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="new")
    def new_trial(self, request):
        # Получаем или создаем запись пробного периода для пользователя
        trial, created = UserTrial.objects.get_or_create(user=request.user)

        # Логика для выдачи триалов
        if not trial.first_trial_date:
            # Если первый триал еще не был выдан
            trial.first_trial_date = timezone.now()
            trial.save()
            return Response({"trial_granted": True}, status=status.HTTP_200_OK)
        elif not trial.second_trial_date:
            # Если первый триал уже выдан, но второй еще нет
            trial.second_trial_date = timezone.now()
            trial.save()
            return Response({"trial_granted": True}, status=status.HTTP_200_OK)
        else:
            # Оба триала уже были выданы
            return Response({"trial_granted": False}, status=status.HTTP_200_OK)
