from django.urls import path
from .views import (
    RecruiterJobListView, RecruiterJobDetailView,
    CandidateScreeningView, RecruiterAnalyticsView,
    ApplicationListView,
)

urlpatterns = [
    path('jobs/', RecruiterJobListView.as_view(), name='recruiter-jobs'),
    path('jobs/<int:pk>/', RecruiterJobDetailView.as_view(), name='recruiter-job-detail'),
    path('screen/', CandidateScreeningView.as_view(), name='candidate-screening'),
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('analytics/', RecruiterAnalyticsView.as_view(), name='recruiter-analytics'),
]
