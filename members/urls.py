from django.urls import path

from . import views

urlpatterns = [
    # 유저 경로
    path("user/register/", views.user_register_view, name="user_register"),
    path("user/home/", views.user_home_view, name="user_home"),
    path("user/login/", views.login_view, name="user_login"),
    path("user/logout/", views.logout_view, name="user_logout"),
    # 회사 경로
    path("company/register/", views.company_register_view, name="company_register"),
    path("company/home/", views.company_home_view, name="company_home"),
    path("company/login/", views.login_view, name="company_login"),
    path("company/logout/", views.logout_view, name="company_logout"),
]
