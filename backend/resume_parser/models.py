from django.db import models
from authentication.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255, blank=True)
    resume_text = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    skills = models.JSONField(default=list)
    education = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    score = models.FloatField(default=0.0)
    ats_score = models.FloatField(default=0.0)
    missing_skills = models.JSONField(default=list)
    keyword_suggestions = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    embedding = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.original_filename}"
