from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/resume/', include('resume_parser.urls')),
    path('api/jobs/', include('job_recommendation.urls')),
    path('api/recruiter/', include('recruiter_screening.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
