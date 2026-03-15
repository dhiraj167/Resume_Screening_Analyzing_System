from django.db import models
from authentication.models import User


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    experience_required = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=50, default='Full-time')
    is_active = models.BooleanField(default=True)
    embedding = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )
    resume = models.ForeignKey('resume_parser.Resume', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    match_score = models.FloatField(default=0.0)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resume', 'job')
        ordering = ['-match_score']

    def __str__(self):
        return f"{self.resume.user.email} -> {self.job.title} ({self.match_score:.1f}%)"
