from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from members.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 리스트 화면 설정
    list_display = ("email", "name", "user_type", "is_active", "is_staff", "last_login", "date_joined")
    list_filter = ("is_active", "is_staff", "user_type")  # 필터링 옵션 추가
    ordering = ("email",)  # 기본 정렬 기준 설정
    search_fields = ("email", "name", "phone_number")  # 검색 가능한 필드

    # 상세 화면 설정
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "개인 정보",
            {"fields": ("name", "user_type", "phone_number", "address", "birthday", "description", "portfolio")},
        ),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("중요한 날짜", {"fields": ("last_login", "date_joined")}),
    )
    # 새 사용자 추가 시 필드 구성
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "user_type",
                    "is_active",
                    "is_staff",
                    "date_joined",
                ),
            },
        ),
    )
