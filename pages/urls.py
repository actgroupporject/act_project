from django.urls import path

from . import views

urlpatterns = [
    path("", views.RecruitMainListView.as_view(), name="recruit_main_list"),
    path("<int:pk>/", views.RecruitMainDetailView.as_view(), name="recruit_main_detail"),
    path("create/", views.RecruitMainCreateView.as_view(), name="recruit_main_create"),
    path("<int:pk>/update/", views.RecruitMainUpdateView.as_view(), name="recruit_main_update"),
    path("<int:pk>/delete/", views.RecruitMainDeleteView.as_view(), name="recruit_main_delete"),
    path("bookmarks/", views.BookMarkListView.as_view(), name="bookmark_list"),
    path("bookmarks/create/", views.BookMarkCreateView.as_view(), name="bookmark_create"),
    path("<int:pk>/add_bookmark/", views.add_bookmark, name="add_bookmark"),
    path("<int:pk>/apply/", views.ApplicationCreateView.as_view(), name="application_create"),
]
