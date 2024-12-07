from django.contrib import admin

from .models import (
    ActorCategory,
    Application,
    Category,
    HowToCategory,
    PoleCategory,
    RecruitDetail,
)


@admin.register(RecruitDetail)
class RecruitDetailAdmin(admin.ModelAdmin):
    list_display = ["title", "work_category", "casting_type", "work_title", "get_d_day"]
    list_filter = ["work_category", "casting_type"]
    search_fields = ["title", "work_title", "requirements"]
