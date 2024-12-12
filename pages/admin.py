from django.contrib import admin
from .models import Application, BookMark, RecruitDetail, RecruitMain


class RecruitDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "get_work_title", "get_work_category"]
    # Uncomment the following line if filtering by `work_category` is needed
    # list_filter = ["recruit_main__work_category"]

    @admin.display(description="Work Title")
    def get_work_title(self, obj):
        return obj.recruit_main.work_title

    @admin.display(description="Work Category")
    def get_work_category(self, obj):
        return obj.recruit_main.work_category


class RecruitMainAdmin(admin.ModelAdmin):
    list_display = ["work_title", "work_category", "deadline", "polecategory", "actorcategory"]
    list_filter = ["work_category", "polecategory", "actorcategory"]


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["recruit", "height", "weight", "age"]
    list_filter = ["recruit__work_category"]


class BookMarkAdmin(admin.ModelAdmin):
    list_display = ["title", "url"]


# Registering models with their respective admin configurations
admin.site.register(RecruitDetail, RecruitDetailAdmin)
admin.site.register(RecruitMain, RecruitMainAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(BookMark, BookMarkAdmin)
