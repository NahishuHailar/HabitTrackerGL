from django.urls import path, re_path, include


urlpatterns = [
    path("/drf-auth/", include("rest_framework.urls")),
    path("djoser/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
