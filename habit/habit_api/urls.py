from django.urls import path
<<<<<<< Updated upstream
from .views import *

urlpatterns = [
    path("api/v1/createuser/", CreateUser.as_view()),
    path("api/v1/user/<uuid:user_id>/", UserRetrieveUpdateDestroyAPIView.as_view()),
    path("api/v1/habits/<uuid:user_id>/", HabitListCreateApiView.as_view()),
=======
from django.views.decorators.cache import cache_page

from .views import (GetUserApiView,
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
)

urlpatterns = [
    path("api/v1/user/", GetUserApiView.as_view(), name="get_user"),
    path("api/v1/user/<uuid:user_id>/", UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
    path("api/v1/habits/<uuid:user_id>/", HabitListCreateAPIView.as_view(), name='user_habits'),
>>>>>>> Stashed changes
    path(
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),name='habit_detail'
    ),
    path("api/v1/habits/<uuid:user_id>/dates/", HabitDatesListAPIView.as_view(), name='habit_dates'),
    path(
<<<<<<< Updated upstream
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/dates/", CurrentHabitdates.as_view()
    ),
    path("api/v1/groups/", HabitGroupListApiView.as_view()),
=======
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/dates/",
        CurrentHabitDatesListAPIView.as_view(), name='current_habit_dates'
    ),
    path("api/v1/groups/", HabitGroupListAPIView.as_view(), name='habit_groups'),
    path("api/v1/avatar/", AvatarListAPIView.as_view(), name='avatar_list'),
    path("api/v1/icons/", IconListListAPIView.as_view(), name='icon_list'),
    path("api/v1/progress/<uuid:user_id>/<int:habit_id>/", HabitProgressAPIView.as_view(), name='habit_progress'),
    path("api/v1/commonprogress/<uuid:user_id>/", CommonHabitProgressAPIView.as_view(), name='common_habit_progress')
>>>>>>> Stashed changes
]
