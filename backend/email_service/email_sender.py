"""
Email Service: Automated rejection email system with personalized templates.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_rejection_email(candidate_name: str, candidate_email: str,
                         job_title: str, missing_skills: list, match_score: float,
                         from_email: str = None) -> bool:
    """
    Send a personalized rejection email to a candidate.
    Returns True if sent successfully, False otherwise.
    """
    reasons = []
    if match_score < 50:
        reasons.append(f"Your overall match score ({match_score:.1f}%) did not meet our minimum threshold.")
    if missing_skills:
        skill_list = ', '.join(missing_skills[:5])
        reasons.append(f"Key skills not found in your resume: {skill_list}.")
    if not reasons:
        reasons.append("We have found other candidates who are a closer match for this role at this time.")

    reasons_text = '\n'.join(f"  • {r}" for r in reasons)

    subject = f"Your Application for {job_title} – Update"

    body = f"""Dear {candidate_name or 'Applicant'},

Thank you for your interest in the {job_title} position and for taking the time to apply.

After careful review of your application, we regret to inform you that we will not be moving forward with your candidacy at this time.

Reasons for this decision:
{reasons_text}

We encourage you to:
  • Strengthen the identified skill areas through courses and projects.
  • Revisit our job board for future openings that may be a better fit.
  • Keep honing your skillset – we'd love to see you apply again!

We appreciate your interest and wish you the very best in your job search.

Warm regards,
The Recruitment Team
AI Resume Screening System
"""

    try:
        sender = from_email if from_email else settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject=subject,
            message=body,
            from_email=sender,
            recipient_list=[candidate_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[Email Error] Failed to send to {candidate_email}: {e}")
        return False
