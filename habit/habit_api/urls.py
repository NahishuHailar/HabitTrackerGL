from django.urls import path
from .views import *

urlpatterns = [
    path("api/v1/cretaeuser/<uuid:pk>/", CreateUser.as_view()),
    path("api/v1/user/<uuid:pk>/", UserRetrieveUpdateDestroyAPIView.as_view()),
    path("api/v1/habits/<uuid:pk>/", HabitListCreateApiView.as_view()),
    path(
        "api/v1/habits/<uuid:uid>/<int:pk>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("api/v1/habits/<uuid:pk>/dates/", Habitdates.as_view()),
    path(
        "api/v1/habits/<uuid:pk>/<int:habit_id>/dates/", CurrentHabitdates.as_view()
    ),
    path("api/v1/groups/", HabitGroupListApiView.as_view()),
]
