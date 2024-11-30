from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("recruit/<int:recruit_id>/", views.RecruitDetailPage.as_view(), name="recruit_detail"),
    # path("recruit/create/", views.RecruitCreateView.as_view(), name="recruit_create"),
]
