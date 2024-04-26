from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/user/<uuid:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/habbits/<uuid:pk>/', HabbitListCreateApiView.as_view()),
    path('api/v1/habbits/<uuid:uid>/<int:pk>/', HabbitRetrieveUpdateDestroyAPIView.as_view()),
    path('api/v1/habbits/<uuid:pk>/dates/', Habbitdates.as_view()),
    path('api/v1/habbits/<uuid:pk>/<int:habbit_id>/dates/', CurrentHabbitdates.as_view()),
    path('api/v1/groups/', HabbitGroupListApiView.as_view()),
]