import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg, Count

from job_recommendation.models import Job, Application
from job_recommendation.serializers import JobSerializer, ApplicationSerializer
from resume_parser.models import Resume
from resume_parser.parser import parse_resume
from email_service.email_sender import send_rejection_email

try:
    from embedding_model import generate_embedding
    from similarity_engine import compute_similarity, rank_candidates, find_skill_gap
except Exception:
    generate_embedding = lambda x: []
    compute_similarity = lambda a, b: 0.0
    rank_candidates = lambda j, c: []
    find_skill_gap = lambda r, q: {'matched': [], 'missing': [], 'match_percentage': 0.0}


class IsRecruiter(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'recruiter'


# ──────────────── JOB POSTING ────────────────

class RecruiterJobListView(generics.ListCreateAPIView):
    """Recruiter: List own jobs and create new ones."""
    permission_classes = (IsRecruiter,)
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

    def perform_create(self, serializer):
        job = serializer.save(recruiter=self.request.user)
        # Generate embedding for job description
        job_text = f"{job.title} {job.description} {' '.join(job.required_skills)}"
        try:
            job.embedding = generate_embedding(job_text)
            job.save()
        except Exception:
            pass


class RecruiterJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsRecruiter,)
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)


# ──────────────── RESUME SCREENING ────────────────

class CandidateScreeningView(APIView):
    """
    Recruiter uploads multiple resumes.
    System extracts, embeds, and ranks them against a job.
    """
    permission_classes = (IsRecruiter,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        job_id = request.data.get('job_id')
        files = request.FILES.getlist('resumes')
        match_threshold = float(request.data.get('threshold', 70.0))

        if not job_id:
            return Response({'error': 'job_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not files:
            return Response({'error': 'No resume files provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = Job.objects.get(id=job_id, recruiter=request.user)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)

        job_embedding = job.embedding or []
        job_text = f"{job.title} {job.description} {' '.join(job.required_skills)}"
        if not job_embedding:
            job_embedding = generate_embedding(job_text)
            if job_embedding:
                job.embedding = job_embedding
                job.save()

        results = []
        rejected = []

        for file_obj in files:
            filename = file_obj.name
            file_content = file_obj.read()
            ext = os.path.splitext(filename)[1].lower()
            if ext not in ['.pdf', '.docx', '.doc', '.txt']:
                continue

            try:
                parsed = parse_resume(file_content, filename)
            except Exception as e:
                continue

            candidate_embedding = []
            if parsed.get('resume_text'):
                try:
                    candidate_embedding = generate_embedding(parsed['resume_text'])
                except Exception:
                    pass

            # Compute similarity
            embedding_score = compute_similarity(job_embedding, candidate_embedding) if candidate_embedding else 0.0
            skill_info = find_skill_gap(parsed.get('skills', []), job.required_skills)
            skill_score = skill_info['match_percentage']
            final_score = round(0.6 * embedding_score + 0.4 * skill_score, 2) if candidate_embedding else skill_score
            
            status_val = 'shortlisted' if final_score >= match_threshold else 'rejected'

            # 1. Save Resume (dummy user link since it's uploaded by recruiter)
            resume_obj = Resume.objects.create(
                user=request.user,  # Associate with recruiter for now
                original_filename=filename,
                resume_text=parsed.get('resume_text', ''),
                name=parsed.get('name', 'Unknown'),
                email=parsed.get('email', ''),
                phone=parsed.get('phone', ''),
                skills=parsed.get('skills', []),
                education=parsed.get('education', []),
                experience=parsed.get('experience', []),
                certifications=parsed.get('certifications', []),
                score=parsed.get('score', 0.0),
                ats_score=parsed.get('ats_score', 0.0),
                embedding=candidate_embedding
            )
            # Save the file to the Resume
            file_obj.seek(0)
            resume_obj.file.save(filename, file_obj)
            
            # Handle rejection emails before saving Application
            rejection_sent = False
            if status_val == 'rejected' and parsed.get('email'):
                rejection_sent = send_rejection_email(
                    candidate_name=parsed.get('name', 'Unknown'),
                    candidate_email=parsed.get('email'),
                    job_title=job.title,
                    missing_skills=skill_info['missing'],
                    match_score=final_score,
                    from_email=job.recruiter.email
                )

            # 2. Save Application
            application_obj, _ = Application.objects.update_or_create(
                resume=resume_obj,
                job=job,
                defaults={
                    'match_score': final_score,
                    'matched_skills': skill_info['matched'],
                    'missing_skills': skill_info['missing'],
                    'status': status_val,
                    'rejection_email_sent': rejection_sent
                }
            )

            candidate_data = {
                'filename': filename,
                'name': parsed.get('name', 'Unknown'),
                'email': parsed.get('email', ''),
                'skills': parsed.get('skills', []),
                'matched_skills': skill_info['matched'],
                'missing_skills': skill_info['missing'],
                'match_score': final_score,
                'resume_score': parsed.get('score', 0),
                'ats_score': parsed.get('ats_score', 0),
                'status': status_val,
                'rejection_email_sent': rejection_sent
            }
            results.append(candidate_data)
            
            if status_val == 'rejected':
                rejected.append(candidate_data)

        # Sort results by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)

        return Response({
            'job': JobSerializer(job).data,
            'total_screened': len(results),
            'shortlisted_count': sum(1 for r in results if r['status'] == 'shortlisted'),
            'rejected_count': len(rejected),
            'threshold': match_threshold,
            'candidates': results,
        })


# ──────────────── ANALYTICS ────────────────

class RecruiterAnalyticsView(APIView):
    """Recruiter Analytics Dashboard: applicant stats, skill distribution."""
    permission_classes = (IsRecruiter,)

    def get(self, request):
        jobs = Job.objects.filter(recruiter=request.user)
        
        job_id = request.query_params.get('job_id')
        applications = Application.objects.filter(job__recruiter=request.user)
        if job_id:
            applications = applications.filter(job_id=job_id)

        # Top candidates
        top_candidates = applications.order_by('-match_score')[:5]

        # Skill distribution across all applications
        all_skills = {}
        for app in applications:
            for skill in app.matched_skills:
                skill_lower = skill.lower()
                all_skills[skill_lower] = all_skills.get(skill_lower, 0) + 1

        sorted_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]

        # Status breakdown
        status_breakdown = {
            'pending': applications.filter(status='pending').count(),
            'shortlisted': applications.filter(status='shortlisted').count(),
            'rejected': applications.filter(status='rejected').count(),
        }

        return Response({
            'total_jobs': jobs.count(),
            'active_jobs': jobs.filter(is_active=True).count(),
            'total_applicants': applications.count(),
            'average_match_score': round(applications.aggregate(Avg('match_score'))['match_score__avg'] or 0, 2),
            'status_breakdown': status_breakdown,
            'top_skills_in_demand': [{'skill': s, 'count': c} for s, c in sorted_skills],
            'top_candidates': ApplicationSerializer(top_candidates, many=True).data,
        })

    def delete(self, request):
        """Clears all screening applications for the recruiter (optionally for a specific job)."""
        job_id = request.query_params.get('job_id')
        applications = Application.objects.filter(job__recruiter=request.user)
        if job_id:
            applications = applications.filter(job_id=job_id)
        
        count, _ = applications.delete()
        return Response({'message': f'Cleared {count} screened candidates.'}, status=status.HTTP_200_OK)


class ApplicationListView(generics.ListAPIView):
    """List all applications for a recruiter's jobs."""
    permission_classes = (IsRecruiter,)
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        job_id = self.request.query_params.get('job_id')
        qs = Application.objects.filter(job__recruiter=self.request.user)
        if job_id:
            qs = qs.filter(job_id=job_id)
        return qs.order_by('-match_score')
