"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'recruits'

urlpatterns = [
    path('', views.RecruitListView.as_view(), name='list'),
    path('<int:recruit_id>/', views.RecruitDetailView.as_view(), name='detail'),
    path('create/', views.RecruitCreateView.as_view(), name='create'),
]

# 프로젝트의 메인 urls.py에 추가
urlpatterns = [
    path("admin/", admin.site.urls),

    # recruits
    path('recruits/', include('recruits.urls')),
    path('common/', include('common.urls')),
    path('', views.map, name='map'),
]