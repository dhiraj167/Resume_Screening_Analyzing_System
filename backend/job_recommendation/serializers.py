from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.SerializerMethodField()
    applicant_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'description', 'required_skills',
            'experience_required', 'salary', 'location', 'job_type',
            'is_active', 'recruiter_name', 'applicant_count', 'created_at',
        ]
        read_only_fields = ('id', 'recruiter_name', 'applicant_count', 'created_at')

    def get_recruiter_name(self, obj):
        return obj.recruiter.get_full_name() or obj.recruiter.email

    def get_applicant_count(self, obj):
        return obj.applications.count()


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    candidate_name = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'job_title', 'company', 'match_score', 'matched_skills',
            'missing_skills', 'status', 'rejection_email_sent', 'created_at',
            'candidate_name', 'candidate_email',
        ]

    def get_job_title(self, obj):
        return obj.job.title

    def get_company(self, obj):
        return obj.job.company

    def get_candidate_name(self, obj):
        return obj.resume.name or obj.resume.user.get_full_name()

    def get_candidate_email(self, obj):
        return obj.resume.email or obj.resume.user.email
