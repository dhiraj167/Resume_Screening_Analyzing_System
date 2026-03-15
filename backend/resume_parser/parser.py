"""
Resume NLP Parser: Extracts structured data from PDF/DOCX/TXT resumes using spaCy.
"""
import re
import io
import spacy

# PDF support (try PyPDF2 first, fall back to pypdf)
try:
    from PyPDF2 import PdfReader
except ImportError:
    from pypdf import PdfReader

from docx import Document

nlp = spacy.load('en_core_web_sm')

# Comprehensive skill keywords
SKILL_KEYWORDS = [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'r', 'go', 'rust',
    'kotlin', 'swift', 'php', 'ruby', 'scala', 'perl', 'matlab', 'dart',
    # Web Frameworks
    'react', 'angular', 'vue', 'nextjs', 'nuxtjs', 'django', 'flask', 'fastapi',
    'express', 'nodejs', 'spring', 'laravel', 'rails', 'asp.net',
    # Data & ML
    'machine learning', 'deep learning', 'neural network', 'nlp', 'computer vision',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'plotly', 'hugging face', 'transformers', 'spacy', 'nltk',
    'opencv', 'pillow', 'xgboost', 'lightgbm', 'catboost',
    # Databases
    'sql', 'mysql', 'postgresql', 'sqlite', 'mongodb', 'redis', 'elasticsearch',
    'cassandra', 'dynamodb', 'firebase', 'supabase', 'oracle',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
    'terraform', 'ansible', 'ci/cd', 'linux', 'git', 'github', 'gitlab',
    # APIs & Tools
    'rest api', 'graphql', 'websocket', 'microservices', 'kafka', 'rabbitmq',
    'nginx', 'apache', 'postman',
    # Design & Other
    'html', 'css', 'tailwindcss', 'bootstrap', 'figma', 'photoshop',
    'project management', 'agile', 'scrum', 'jira', 'tableau', 'power bi',
    'excel', 'word', 'powerpoint',
]


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        reader = PdfReader(io.BytesIO(file_content))
        text = ''
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + '\n'
        return text.strip()
    except Exception as e:
        return ''


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX bytes."""
    try:
        doc = Document(io.BytesIO(file_content))
        text = '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        return ''


def extract_email(text: str) -> str:
    """Extract email from text."""
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ''


def extract_phone(text: str) -> str:
    """Extract phone number from text."""
    pattern = r'(\+?\d[\d\s\-().]{7,}\d)'
    matches = re.findall(pattern, text)
    return matches[0].strip() if matches else ''


def extract_name(text: str) -> str:
    """
    Extract name using heuristic (first clean line) or spaCy NER.
    """
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 1. Strong Heuristic: First line is very often the candidate's name
    if lines:
        first = lines[0]
        bad_words = ['resume', 'cv', 'curriculum', 'email', 'phone', 'address', 'mobile']
        # If it's a short line, no weird symbols, and doesn't contain words like "resume"
        if len(first.split()) <= 4 and not any(c in first for c in ['@', '|', '/', '\\', ':', '-', '(', ')', '0', '1']):
            if not any(bw in first.lower() for bw in bad_words):
                return first.title() if first.isupper() else first

    # 2. Fallback to spaCy NER
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            name = ent.text.strip()
            # Ignore obvious false positives
            if name.lower() not in ['email', 'phone', 'address', 'github', 'linkedin', 'resume'] and len(name.split()) <= 4:
                return name.title() if name.isupper() else name

    # 3. Final Fallback: just return the first line if it's somewhat sane
    if lines:
        first = lines[0]
        if len(first.split()) <= 5 and not any(c in first for c in ['@', '|', '\\']):
            return first.title() if first.isupper() else first
            
    return ''


def extract_skills(text: str) -> list:
    """Extract skills by matching against known skill keywords."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        # Use word boundary matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title() if len(skill) <= 3 else skill.capitalize())
    return list(dict.fromkeys(found))  # deduplicate while preserving order


def extract_education(text: str) -> list:
    """Extract education entries."""
    education = []
    degrees = [
        'b.tech', 'b.e', 'btech', 'be ', 'm.tech', 'mtech', 'master', 'bachelor',
        'mba', 'mca', 'bca', 'b.sc', 'b.com', 'm.sc', 'phd', 'diploma',
        'bachelor of', 'master of', 'doctor of', 'b.s.', 'm.s.'
    ]
    text_lower = text.lower()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(deg in line_lower for deg in degrees):
            entry = line.strip()
            if i + 1 < len(lines) and lines[i + 1].strip():
                entry += ' | ' + lines[i + 1].strip()
            if entry:
                education.append(entry[:200])
    return education[:5]


def extract_experience(text: str) -> list:
    """Extract experience entries using pattern matching."""
    experience = []
    exp_keywords = ['experience', 'work history', 'employment', 'intern', 'project']
    lines = text.split('\n')
    in_section = False
    for line in lines:
        line_strip = line.strip()
        if any(kw in line.lower() for kw in exp_keywords) and len(line_strip) < 50:
            in_section = True
            continue
        if in_section and line_strip:
            # Stop at next major section
            if line_strip.isupper() and len(line_strip) > 3:
                in_section = False
            else:
                experience.append(line_strip)
        if len(experience) >= 10:
            break
    return experience


def extract_certifications(text: str) -> list:
    """Extract certifications from resume."""
    cert_keywords = ['certified', 'certification', 'certificate', 'aws certified',
                     'google certified', 'microsoft certified', 'coursera', 'udemy', 'edx']
    certs = []
    lines = text.split('\n')
    for line in lines:
        if any(kw in line.lower() for kw in cert_keywords):
            c = line.strip()
            if c and len(c) < 200:
                certs.append(c)
    return certs[:10]


def calculate_resume_score(parsed_data: dict) -> float:
    """Score the resume from 0-100 based on completeness and quality."""
    score = 0.0
    weights = {
        'name': 10,
        'email': 10,
        'phone': 5,
        'skills': 30,
        'education': 20,
        'experience': 20,
        'certifications': 5,
    }
    if parsed_data.get('name'): score += weights['name']
    if parsed_data.get('email'): score += weights['email']
    if parsed_data.get('phone'): score += weights['phone']
    skills = parsed_data.get('skills', [])
    score += min(weights['skills'], len(skills) * 3)
    if parsed_data.get('education'): score += weights['education']
    exp = parsed_data.get('experience', [])
    score += min(weights['experience'], len(exp) * 4)
    if parsed_data.get('certifications'): score += weights['certifications']
    return min(round(score, 1), 100.0)


def calculate_ats_score(text: str, skills: list) -> float:
    """Check ATS compatibility: formatting, keywords, sections."""
    score = 0.0
    # Section headers check
    sections = ['education', 'experience', 'skills', 'projects', 'summary', 'objective']
    text_lower = text.lower()
    found_sections = sum(1 for s in sections if s in text_lower)
    score += min(40, found_sections * 7)
    # Keyword density
    word_count = len(text.split())
    if word_count > 200:
        score += 20
    if word_count > 400:
        score += 10
    # Skills present
    score += min(30, len(skills) * 2)
    return min(round(score, 1), 100.0)


def get_improvement_suggestions(parsed_data: dict, text: str) -> list:
    """Generate improvement suggestions based on resume analysis."""
    suggestions = []
    if not parsed_data.get('phone'):
        suggestions.append("Add your phone number for easier recruiter contact.")
    if len(parsed_data.get('skills', [])) < 8:
        suggestions.append("Include more technical skills relevant to your target role.")
    if not parsed_data.get('certifications'):
        suggestions.append("Consider adding professional certifications or online courses.")
    word_count = len(text.split())
    if word_count < 200:
        suggestions.append("Your resume seems too short. Add more detail to experience and projects.")
    if word_count > 1000:
        suggestions.append("Your resume is quite long. Consider condensing to 1-2 pages.")
    text_lower = text.lower()
    if 'summary' not in text_lower and 'objective' not in text_lower:
        suggestions.append("Add a professional summary or objective statement at the top.")
    if 'projects' not in text_lower:
        suggestions.append("Include a projects section to showcase hands-on experience.")
    if not re.search(r'github\.com', text_lower) and not re.search(r'linkedin\.com', text_lower):
        suggestions.append("Add links to your GitHub and LinkedIn profiles.")
    vague_phrases = ['worked with', 'helped with', 'involved in', 'responsible for']
    for phrase in vague_phrases:
        if phrase in text_lower:
            suggestions.append(
                f"Replace vague phrase '{phrase}' with quantified achievements "
                f"(e.g., 'Built X using Y, increasing Z by N%')."
            )
            break
    return suggestions


def parse_resume(file_content: bytes, filename: str) -> dict:
    """
    Main function to parse a resume file and return structured data.
    Supports PDF, DOCX, DOC, and TXT formats.
    """
    filename_lower = filename.lower()
    if filename_lower.endswith('.pdf'):
        text = extract_text_from_pdf(file_content)
    elif filename_lower.endswith(('.docx', '.doc')):
        text = extract_text_from_docx(file_content)
    elif filename_lower.endswith('.txt'):
        text = file_content.decode('utf-8', errors='ignore')
    else:
        text = file_content.decode('utf-8', errors='ignore')

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    certifications = extract_certifications(text)

    parsed_data = {
        'resume_text': text,
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'education': education,
        'experience': experience,
        'certifications': certifications,
    }

    score = calculate_resume_score(parsed_data)
    ats_score = calculate_ats_score(text, skills)
    suggestions = get_improvement_suggestions(parsed_data, text)

    parsed_data['score'] = score
    parsed_data['ats_score'] = ats_score
    parsed_data['improvement_suggestions'] = suggestions

    return parsed_data
