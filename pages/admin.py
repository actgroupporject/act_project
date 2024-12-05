from django.contrib import admin

from .models import RecruitDetail, RecruitMain


class RecruitDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "get_work_category", "title", "get_work_title", "director")
    list_filter = ("recruitmain__work_category",)

    @admin.display(description="Work Category")
    def get_work_category(self, obj):
        return obj.recruitmain.work_category

    @admin.display(description="Work Title")
    def get_work_title(self, obj):
        return obj.recruitmain.work_title


admin.site.register(RecruitDetail, RecruitDetailAdmin)
