from django.contrib import admin
from .models import (Category, PoleCategory, ActorCategory, 
                    HowToCategory, RecruitPage, RecruitDetail, Apply)

@admin.register(RecruitDetail)
class RecruitDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'pole_category', 'actor_category', 
                   'title_name', 'get_d_day']
    list_filter = ['pole_category', 'actor_category']
    search_fields = ['title', 'title_name', 'description']

@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'recruit', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant_name', 'email', 'phone_number']