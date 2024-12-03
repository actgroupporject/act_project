from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.RecruitListView.as_view(), name="list"),
    path("<int:pk>/", views.RecruitDetailView.as_view(), name="detail"),
    path("create/", views.RecruitCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.RecruitUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.RecruitDeleteView.as_view(), name="delete"),
    path("category/<str:category>/", views.RecruitListView.as_view(), name="category_list"),
    path("pole/<str:pole_category>/", views.RecruitListView.as_view(), name="pole_list"),
    path("actor/<str:actor_category>/", views.RecruitListView.as_view(), name="actor_list"),
]
