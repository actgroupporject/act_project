from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from members.models import Company, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "name", "is_active", "is_staff")
    ordering = ("email",)  # User 모델에는 'username' 필드가 없으므로 'email'로 대체
    search_fields = ("email", "name")  # 검색 필드 추가


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_active", "is_staff")
    search_fields = ("email", "name")
