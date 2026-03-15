from django.urls import path
from .views import JobListView, JobDetailView, JobRecommendationView, SkillGapView

urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('recommendations/', JobRecommendationView.as_view(), name='job-recommendations'),
    path('skill-gap/', SkillGapView.as_view(), name='skill-gap'),
]
