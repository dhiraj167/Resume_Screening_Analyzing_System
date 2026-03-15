import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from .models import Resume
from .serializers import ResumeSerializer
from .parser import parse_resume
from embedding_model import generate_embedding


class ResumeUploadView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        filename = file_obj.name
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        ext = os.path.splitext(filename)[1].lower()
        if ext not in allowed_extensions:
            return Response(
                {'error': f'Unsupported file type. Please upload PDF, DOCX, or TXT.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_content = file_obj.read()
        try:
            parsed = parse_resume(file_content, filename)
        except Exception as e:
            return Response({'error': f'Failed to parse resume: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Generate embedding from resume text
        embedding = []
        if parsed.get('resume_text'):
            try:
                embedding = generate_embedding(parsed['resume_text'])
            except Exception:
                pass

        # Save resume record
        resume = Resume(
            user=request.user,
            original_filename=filename,
            resume_text=parsed.get('resume_text', ''),
            name=parsed.get('name', ''),
            email=parsed.get('email', ''),
            phone=parsed.get('phone', ''),
            skills=parsed.get('skills', []),
            education=parsed.get('education', []),
            experience=parsed.get('experience', []),
            certifications=parsed.get('certifications', []),
            score=parsed.get('score', 0.0),
            ats_score=parsed.get('ats_score', 0.0),
            improvement_suggestions=parsed.get('improvement_suggestions', []),
            embedding=embedding,
        )
        file_obj.seek(0)
        resume.file.save(filename, file_obj)
        resume.save()

        serializer = ResumeSerializer(resume)
        return Response({
            'message': 'Resume uploaded and analyzed successfully.',
            'resume': serializer.data
        }, status=status.HTTP_201_CREATED)


class ResumeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeAnalysisView(APIView):
    """Get detailed analysis and keyword optimization suggestions for a resume."""
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            resume = Resume.objects.get(pk=pk, user=request.user)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Keyword optimization suggestions
        keyword_suggestions = self._get_keyword_suggestions(resume)

        return Response({
            'id': resume.id,
            'score': resume.score,
            'ats_score': resume.ats_score,
            'skills': resume.skills,
            'missing_skills': resume.missing_skills,
            'education': resume.education,
            'experience': resume.experience,
            'certifications': resume.certifications,
            'improvement_suggestions': resume.improvement_suggestions,
            'keyword_suggestions': keyword_suggestions,
        })

    def _get_keyword_suggestions(self, resume):
        """Generate actionable keyword improvement examples."""
        suggestions = []
        replacements = [
            ("worked with data", "Built machine learning models using Python and Scikit-learn"),
            ("helped with", "Spearheaded development of"),
            ("responsible for", "Engineered and maintained"),
            ("assisted in", "Collaborated to deliver"),
            ("good knowledge of", "Proficient in"),
        ]
        text_lower = resume.resume_text.lower()
        for old, new in replacements:
            if old in text_lower:
                suggestions.append({'original': old, 'improved': new})
        return suggestions
