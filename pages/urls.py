from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"recruits", views.RecruitViewSet)
router.register(r"applications", views.ApplicationViewSet)
router.register(r"actors", views.ActorViewSet)
router.register(r"actor-images", views.ActorImageViewSet)
router.register(r"actor-videos", views.ActorVideoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
