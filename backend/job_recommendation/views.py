import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from resume_parser.models import Resume
from resume_parser.skill_resources import get_skill_gap_resources

try:
    from embedding_model import generate_embedding
    from similarity_engine import compute_similarity, rank_candidates, find_skill_gap
except Exception:
    generate_embedding = lambda x: []
    compute_similarity = lambda a, b: 0.0
    rank_candidates = lambda j, c: []
    find_skill_gap = lambda r, q: {'matched': [], 'missing': r, 'match_percentage': 0.0}


class IsJobSeeker(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'job_seeker'


class JobListView(generics.ListAPIView):
    """List all active jobs (job seekers can search and browse)."""
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        search = self.request.query_params.get('q')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__icontains=search)
            )
        return queryset


class JobDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobSerializer
    queryset = Job.objects.filter(is_active=True)


class JobRecommendationView(APIView):
    """Recommend jobs based on resume embedding similarity."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Get the user's latest resume (or a specific one)
        resume_id = request.query_params.get('resume_id')
        try:
            if resume_id:
                resume = Resume.objects.get(id=resume_id, user=request.user)
            else:
                resume = Resume.objects.filter(user=request.user).first()
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not resume:
            return Response({'error': 'Please upload a resume first.'}, status=status.HTTP_400_BAD_REQUEST)

        jobs = Job.objects.filter(is_active=True)
        if not jobs.exists():
            return Response({'recommendations': [], 'message': 'No jobs available yet.'})

        # Score each job based on skill overlap (fast) and embedding similarity
        recommendations = []
        resume_embedding = resume.embedding or []

        for job in jobs:
            # Compute skill-based gap
            skill_info = find_skill_gap(resume.skills, job.required_skills)
            match_percentage = skill_info['match_percentage']

            # If resume has embedding and job has embedding, use cosine similarity
            if resume_embedding and job.embedding:
                embedding_score = compute_similarity(resume_embedding, job.embedding)
                # Blend: 60% embedding, 40% skill overlap
                final_score = round(0.6 * embedding_score + 0.4 * match_percentage, 2)
            else:
                final_score = match_percentage

            recommendations.append({
                'job': JobSerializer(job).data,
                'match_score': final_score,
                'matched_skills': skill_info['matched'],
                'missing_skills': skill_info['missing'],
            })

        # Sort by match score descending
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return Response({'recommendations': recommendations[:15]})


class SkillGapView(APIView):
    """Detect skill gaps and return learning resources."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        resume_id = request.query_params.get('resume_id')
        job_id = request.query_params.get('job_id')

        if not resume_id or not job_id:
            return Response({'error': 'resume_id and job_id required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            job = Job.objects.get(id=job_id)
        except (Resume.DoesNotExist, Job.DoesNotExist):
            return Response({'error': 'Resume or Job not found.'}, status=status.HTTP_404_NOT_FOUND)

        skill_info = find_skill_gap(resume.skills, job.required_skills)
        learning_resources = get_skill_gap_resources(skill_info['missing'])

        return Response({
            'job_title': job.title,
            'match_percentage': skill_info['match_percentage'],
            'matched_skills': skill_info['matched'],
            'missing_skills': skill_info['missing'],
            'learning_resources': learning_resources,
        })
