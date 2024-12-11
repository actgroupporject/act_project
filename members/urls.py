from django.urls import path

from .views import (
    CompanyRegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserRegisterAPIView,
)

urlpatterns = [
    # 유저 경로
    path("auth/sign-up/", UserRegisterAPIView.as_view(), name="user_register"),  # 수정됨
    # 회사 경로
    path("companies/sign-up/", CompanyRegisterAPIView.as_view(), name="company_register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
]
