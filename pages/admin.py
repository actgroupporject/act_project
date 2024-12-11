from django.contrib import admin

from .models import RecruitDetail, RecruitMain


@admin.register(RecruitDetail)
class RecruitDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "get_work_category", "get_work_title", "casting_type", "director", "get_d_day")
    list_filter = ("recruitmain__work_category", "casting_type")
    search_fields = ["title", "recruitmain__work_title", "requirements"]

    @admin.display(description="Work Category")
    def get_work_category(self, obj):
        return obj.recruitmain.work_category

    @admin.display(description="Work Title")
    def get_work_title(self, obj):
        return obj.recruitmain.work_title
