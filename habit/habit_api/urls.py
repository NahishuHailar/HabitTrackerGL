from django.urls import path
from .views import *

urlpatterns = [
    path("api/v1/createuser/", CreateUser.as_view()),
    path("api/v1/user/<uuid:user_id>/", UserRetrieveUpdateDestroyAPIView.as_view()),
    path("api/v1/habits/<uuid:user_id>/", HabitListCreateApiView.as_view()),
    path(
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("api/v1/habits/<uuid:user_id>/dates/", Habitdates.as_view()),
    path(
        "api/v1/habits/<uuid:user_id>/<int:habit_id>/dates/", CurrentHabitdates.as_view()
    ),
    path("api/v1/groups/", HabitGroupListApiView.as_view()),
]
