from django.urls import path

from . import views

app_name = "pages"

from django.urls import path
from . import views

app_name = 'recruits'

urlpatterns = [
    # 채용 공고 목록
    path('', views.RecruitListView.as_view(), name='list'),

    # 채용 공고 상세
    path('<int:pk>/', views.RecruitDetailView.as_view(), name='detail'),

    # 채용 공고 생성/수정/삭제
    path('create/', views.RecruitCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.RecruitUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.RecruitDeleteView.as_view(), name='delete'),

    # 지원 관련
    path('<int:recruit_pk>/apply/', views.ApplyCreateView.as_view(), name='apply'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),

    # 카테고리별 필터링
    path('category/<str:category>/', views.RecruitListView.as_view(), name='category_list'),
    path('pole/<str:pole_category>/', views.RecruitListView.as_view(), name='pole_list'),
    path('actor/<str:actor_category>/', views.RecruitListView.as_view(), name='actor_list'),
]