from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (GetUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    HabitListCreateAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    HabitDatesListAPIView,
    CurrentHabitDatesListAPIView,
    HabitGroupListAPIView,
    AvatarListAPIView,
    HabitProgressAPIView,
    CommonHabitProgressAPIView,
    IconListListAPIView,
    get_error
)

urlpatterns = [
    path("api/v1/user/", GetUserAPIView.as_view(), name="get_user"),
    path("api/v1/user/<uuid:user_id>/", UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
    path("api/v1/habits/<uuid:user_id>/", HabitListCreateAPIView.as_view(), name='user_habits'),
    path(
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),name='habit_detail'
    ),
    path("api/v1/habits/<uuid:user_id>/dates/", HabitDatesListAPIView.as_view(), name='habit_dates'),
    path(

        "api/v1/habits/<uuid:user_id>/<int:habit_id>/dates/",
        CurrentHabitDatesListAPIView.as_view(), name='current_habit_dates'
    ),
    path("api/v1/groups/", HabitGroupListAPIView.as_view(), name='habit_groups'),
    path("api/v1/avatar/", AvatarListAPIView.as_view(), name='avatar_list'),
    path("api/v1/icons/", IconListListAPIView.as_view(), name='icon_list'),
    path("api/v1/progress/<uuid:user_id>/<int:habit_id>/", HabitProgressAPIView.as_view(), name='habit_progress'),
    path("api/v1/commonprogress/<uuid:user_id>/", CommonHabitProgressAPIView.as_view(), name='common_habit_progress'),
    path("api/v1/sentry/", get_error)
]
