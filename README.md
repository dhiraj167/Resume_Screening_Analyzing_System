# Resume Analyzer Project — Setup Instructions

## Prerequisites
- Python 3.10+ with a virtual environment at `./myenv`
- Node.js 18+ for the frontend

---

## Backend Setup

```bash
# Activate virtual environment
.\myenv\Scripts\activate   # (Windows)
source myenv/bin/activate  # (Linux/Mac)

# Install Python dependencies
pip install -r backend/requirements.txt

# Download spaCy NLP model
python -m spacy download en_core_web_sm

# Run Django migrations
cd backend
python manage.py migrate

# (Optional) Create admin superuser
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

Backend runs at: **http://localhost:8000**

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## Environment Configuration

**Email (SMTP)** — Edit `backend/resume_analyzer_backend/settings.py`:
```python
EMAIL_HOST_USER     = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-gmail-app-password'
```

**PostgreSQL (Optional)** — Replace the `DATABASES` section in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resume_analyzer_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## API Endpoints

| Endpoint                        | Method | Auth | Description                         |
|---------------------------------|--------|------|-------------------------------------|
| `/api/auth/register/`           | POST   | No   | Register as Job Seeker / Recruiter  |
| `/api/auth/login/`              | POST   | No   | Login and get JWT tokens            |
| `/api/auth/profile/`            | GET    | Yes  | Get / update user profile           |
| `/api/resume/upload/`           | POST   | Yes  | Upload & analyze a resume           |
| `/api/resume/list/`             | GET    | Yes  | List your resumes                   |
| `/api/resume/<id>/analysis/`    | GET    | Yes  | Get detailed resume analysis        |
| `/api/jobs/`                    | GET    | Yes  | Browse all jobs (search with `?q=`) |
| `/api/jobs/recommendations/`    | GET    | Yes  | AI job recommendations              |
| `/api/jobs/skill-gap/`          | GET    | Yes  | Skill gap + learning resources      |
| `/api/recruiter/jobs/`          | POST   | Yes  | Create a job post (recruiter only)  |
| `/api/recruiter/screen/`        | POST   | Yes  | Bulk resume screening               |
| `/api/recruiter/analytics/`     | GET    | Yes  | Recruiter analytics dashboard       |
| `/api/token/refresh/`           | POST   | No   | Refresh JWT access token            |

---

## Project Structure

```
Resume_Project/
├── backend/
│   ├── authentication/       # Custom user model, JWT auth
│   ├── resume_parser/        # Resume upload, NLP analysis, ATS check
│   ├── job_recommendation/   # Job listing, embeddings, recommendations
│   ├── recruiter_screening/  # Bulk screening, ranking, analytics
│   ├── email_service/        # SMTP rejection emails
│   └── resume_analyzer_backend/  # Django settings, URLs
│
├── frontend/
│   └── src/
│       ├── pages/            # Landing, Login, Signup, Dashboards
│       ├── components/       # ProtectedRoute
│       ├── context/          # AuthContext (JWT state)
│       └── services/         # api.js (all backend calls)
│
├── ml_models/
│   ├── embedding_model.py    # all-MiniLM-L6-v2 sentence embeddings
│   └── similarity_engine.py  # Cosine similarity scoring
│
└── myenv/                    # Virtual environment (not in repo)
```
