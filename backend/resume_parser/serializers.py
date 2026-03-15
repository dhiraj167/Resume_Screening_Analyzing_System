from rest_framework import serializers
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id', 'original_filename', 'name', 'email', 'phone',
            'skills', 'education', 'experience', 'certifications',
            'score', 'ats_score', 'missing_skills',
            'improvement_suggestions', 'keyword_suggestions',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields
