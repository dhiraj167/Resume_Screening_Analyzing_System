from django.core.management.base import BaseCommand
from job_recommendation.models import Job
from authentication.models import User
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../ml_models')))
from embedding_model import generate_embedding
import random

class Command(BaseCommand):
    help = 'Seeds the database with various job postings'

    def handle(self, *args, **options):
        # Create a default recruiter if one doesn't exist
        recruiter, created = User.objects.get_or_create(
            email='recruiter@example.com',
            defaults={
                'username': 'recruiter_demo',
                'role': 'recruiter',
                'first_name': 'Tech',
                'last_name': 'Recruiter'
            }
        )
        if created:
            recruiter.set_password('password123')
            recruiter.save()
            self.stdout.write(self.style.SUCCESS('Created default recruiter (recruiter@example.com / password123)'))

        jobs_data = [
            {
                "title": "Senior Frontend Developer",
                "company": "TechCorp",
                "description": "We are looking for an experienced Frontend Developer to lead our UI team. You will be responsible for building complex web applications using React, optimizing frontend performance, and mentoring junior developers.",
                "required_skills": ["React", "JavaScript", "TypeScript", "HTML", "CSS", "TailwindCSS"],
                "experience_required": "4-6 years",
                "salary": "₹15,00,000 - ₹25,00,000",
                "location": "Bengaluru",
                "job_type": "Full-time"
            },
            {
                "title": "Data Scientist",
                "company": "AI Solutions",
                "description": "Join our AI research team to develop state-of-the-art predictive models. You'll work with large datasets, train machine learning models, and deploy scalable solutions.",
                "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL", "Pandas"],
                "experience_required": "2-4 years",
                "salary": "₹12,00,000 - ₹20,00,000",
                "location": "Hyderabad",
                "job_type": "Full-time"
            },
            {
                "title": "DevOps Engineer",
                "company": "Cloud Systems",
                "description": "We need a DevOps expert to manage our cloud infrastructure, optimize our CI/CD pipelines, and ensure system reliability and security.",
                "required_skills": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux"],
                "experience_required": "3-5 years",
                "salary": "₹18,00,000 - ₹30,00,000",
                "location": "Pune",
                "job_type": "Hybrid"
            },
            {
                "title": "Backend Python Developer",
                "company": "FinTech Startup",
                "description": "Build high-performance, secure backend services for our financial platform. You'll design REST APIs and work closely with product teams.",
                "required_skills": ["Python", "Django", "PostgreSQL", "REST API", "Redis", "Git"],
                "experience_required": "1-3 years",
                "salary": "₹8,00,000 - ₹15,00,000",
                "location": "Mumbai",
                "job_type": "Remote"
            },
            {
                "title": "UX/UI Designer",
                "company": "Creative Agency",
                "description": "Looking for a creative product designer to craft beautiful and intuitive user experiences. You'll conduct user research and build interactive prototypes.",
                "required_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Adobe XD", "HTML/CSS"],
                "experience_required": "2-5 years",
                "salary": "₹10,00,000 - ₹18,00,000",
                "location": "Delhi",
                "job_type": "Full-time"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Vision AI",
                "description": "Develop and deploy deep learning models for computer vision applications. Strong background in deep neural networks and PyTorch is required.",
                "required_skills": ["Python", "Deep Learning", "PyTorch", "Computer Vision", "C++", "Docker"],
                "experience_required": "3-6 years",
                "salary": "₹20,00,000 - ₹35,00,000",
                "location": "Bengaluru",
                "job_type": "Full-time"
            },
            {
                "title": "Full Stack MERN Developer",
                "company": "WebInnovators",
                "description": "Seeking a MERN stack developer to build scalable web applications from scratch. You will handle both frontend interfaces and backend APIs.",
                "required_skills": ["MongoDB", "Express", "React", "Node.js", "JavaScript"],
                "experience_required": "2-4 years",
                "salary": "₹12,00,000 - ₹18,00,000",
                "location": "Remote",
                "job_type": "Full-time"
            },
            {
                "title": "Cybersecurity Analyst",
                "company": "SecureNetworks",
                "description": "Join our SOC team to monitor, detect, and respond to security incidents. Conduct vulnerability assessments and penetration testing.",
                "required_skills": ["Networking", "Python", "Linux", "Penetration Testing", "SIEM", "Security"],
                "experience_required": "2-5 years",
                "salary": "₹9,00,000 - ₹16,00,000",
                "location": "Chennai",
                "job_type": "Full-time"
            },
            {
                "title": "Android Developer",
                "company": "MobileFirst",
                "description": "Build high-quality Android applications using Kotlin and Jetpack Compose. Focus on performance, clean architecture, and user experience.",
                "required_skills": ["Kotlin", "Android Studio", "Jetpack Compose", "Java", "Mobile Development"],
                "experience_required": "1-4 years",
                "salary": "₹10,00,000 - ₹16,00,000",
                "location": "Hyderabad",
                "job_type": "Hybrid"
            },
            {
                "title": "Product Manager",
                "company": "SaaS Platform",
                "description": "Drive the product vision and roadmap. Translate business requirements into technical specs and lead cross-functional teams to deliver value.",
                "required_skills": ["Product Management", "Agile", "Scrum", "Jira", "Data Analysis", "Roadmapping"],
                "experience_required": "4-7 years",
                "salary": "₹20,00,000 - ₹30,00,000",
                "location": "Bengaluru",
                "job_type": "Full-time"
            },
            {
                "title": "iOS Developer",
                "company": "AppVentures",
                "description": "Create amazing iOS experiences using Swift and SwiftUI. You'll work on high-traffic consumer applications.",
                "required_skills": ["Swift", "iOS", "SwiftUI", "Objective-C", "Mobile Development"],
                "experience_required": "2-5 years",
                "salary": "₹12,00,000 - ₹22,00,000",
                "location": "Pune",
                "job_type": "Full-time"
            },
            {
                "title": "Data Engineer",
                "company": "BigData Corp",
                "description": "Design, build, and maintain scalable data pipelines. Experience with Spark, Airflow, and cloud data warehouses is highly desired.",
                "required_skills": ["SQL", "Python", "Apache Spark", "Airflow", "ETL", "AWS"],
                "experience_required": "3-5 years",
                "salary": "₹15,00,000 - ₹25,00,000",
                "location": "Noida",
                "job_type": "Hybrid"
            },
            {
                "title": "Backend Java Engineer",
                "company": "Banking Solutions",
                "description": "Develop mission-critical banking applications. Deep expertise in Java, Spring Boot, and microservices architecture is required.",
                "required_skills": ["Java", "Spring Boot", "Microservices", "SQL", "Hibernate", "Kafka"],
                "experience_required": "5-8 years",
                "salary": "₹25,00,000 - ₹40,00,000",
                "location": "Mumbai",
                "job_type": "Full-time"
            },
            {
                "title": "QA Automation Engineer",
                "company": "QualityNet",
                "description": "Ensure product quality by designing and implementing automated test frameworks for web and mobile applications.",
                "required_skills": ["Selenium", "Python", "Java", "Test Automation", "Cypress", "Appium"],
                "experience_required": "2-4 years",
                "salary": "₹8,00,000 - ₹14,00,000",
                "location": "Remote",
                "job_type": "Full-time"
            },
            {
                "title": "Business Analyst",
                "company": "Consulting Group",
                "description": "Bridge the gap between business needs and technological solutions. You will gather requirements, create BRDs, and work with engineering teams.",
                "required_skills": ["Business Analysis", "Requirements Gathering", "SQL", "Excel", "Agile", "UML"],
                "experience_required": "3-6 years",
                "salary": "₹10,00,000 - ₹18,00,000",
                "location": "Gurgaon",
                "job_type": "Full-time"
            }
        ]

        count = 0
        self.stdout.write("Seeding jobs... This might take a minute as AI embeddings are generated.")
        
        for idx, data in enumerate(jobs_data):
            # Check if job already exists to avoid duplicates
            if Job.objects.filter(title=data['title'], company=data['company']).exists():
                self.stdout.write(f"Job '{data['title']}' already exists, skipping.")
                continue

            # Generate embedding
            text_for_embedding = f"{data['title']} {data['required_skills']} {data['description']}"
            embedding = []
            try:
                embedding = generate_embedding(text_for_embedding)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not generate embedding for {data['title']}: {e}"))

            Job.objects.create(
                recruiter=recruiter,
                title=data['title'],
                company=data['company'],
                description=data['description'],
                required_skills=data['required_skills'],
                experience_required=data['experience_required'],
                salary=data['salary'],
                location=data['location'],
                job_type=data['job_type'],
                embedding=embedding
            )
            count += 1
            if count % 5 == 0:
                self.stdout.write(f"Created {count} jobs...")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new jobs!'))
