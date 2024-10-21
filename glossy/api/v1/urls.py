from django.urls import path
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from api.v1.views.views import (GetUserAPIView, LifeSpheresViewSet,
    UserRetrieveUpdateDestroyAPIView,
    HabitListCreateAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    HabitDatesListAPIView,
    CurrentHabitDatesListAPIView,
    HabitGroupListAPIView,
    AvatarListAPIView,
    HabitProgressPagAPIView,
    CommonHabitProgressPagAPIView,
    IconListListAPIView,
    AvatarGroupListAPIView,
    HabitProgressAPIView,
    CommonHabitProgressAPIView,
    HabitTemplateViewSet

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
    path("api/v1/avatargroup/", AvatarGroupListAPIView.as_view(), name='avatargroup_list'),
    path("api/v1/icons/", IconListListAPIView.as_view(), name='icon_list'),
    path("api/v1/progresspag/<uuid:user_id>/<int:habit_id>/", HabitProgressPagAPIView.as_view(), name='habit_progress'),
    path("api/v1/commonprogresspag/<uuid:user_id>/", CommonHabitProgressPagAPIView.as_view(), name='common_habit_progress'),
    path("api/v1/progress/<uuid:user_id>/<int:habit_id>/", HabitProgressAPIView.as_view(), name='habit_progress'),
    path("api/v1/commonprogress/<uuid:user_id>/", CommonHabitProgressAPIView.as_view(), name='common_habit_progress'),
  
]


router = DefaultRouter()
router.register(r'api/v1/habit-templates', HabitTemplateViewSet, basename='habit-template')
router.register(r'api/v1/life-spheres', LifeSpheresViewSet, basename='life-spheres')

urlpatterns += router.urls
