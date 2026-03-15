import os
import random

resumes_dir = r"c:\Users\pandi\Downloads\Resume_Project\database\sample_resumes"
os.makedirs(resumes_dir, exist_ok=True)

# Count existing resumes to continue numbering
existing_files = [f for f in os.listdir(resumes_dir) if f.endswith('.txt') and getattr(f, 'startswith', lambda x: False)(tuple('0123456789'))]
start_idx = 16

names_first = ["Amit", "Rohit", "Neha", "Priya", "Kavita", "Suresh", "Vikram", "Anita", "Ravi", "Manoj",
               "Deepika", "Arjun", "Rajesh", "Sunita", "Anjali", "Gaurav", "Pooja", "Rahul", "Sonia", "Karan",
               "Aisha", "Bhavin", "Chirag", "Divya", "Esha", "Farhan", "Geeta", "Harsh", "Isha", "Jatin"]

names_last = ["Sharma", "Verma", "Gupta", "Singh", "Patel", "Mehta", "Jain", "Reddy", "Rao", "Nair",
              "Krishna", "Kumar", "Das", "Bose", "Ghosh", "Iyer", "Sen", "Bhatt", "Desai", "Joshi",
              "Kaur", "Malhotra", "Nath", "Ojha", "Pandey", "Qureshi", "Rastogi", "Sethi", "Thakur", "Yadav"]

roles = [
    {"role": "Frontend Developer", "skills": ["React", "Vue", "Angular", "JavaScript", "TypeScript", "HTML", "CSS", "TailwindCSS"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Backend Developer", "skills": ["Python", "Django", "Node.js", "Express", "Java", "Spring Boot", "Go", "SQL", "PostgreSQL", "MongoDB"], "prefixes": ["Junior", "Senior", "Lead", "Principal"]},
    {"role": "Full Stack Developer", "skills": ["React", "Node.js", "Express", "MongoDB", "Python", "Django", "JavaScript", "AWS"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Data Scientist", "skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "TensorFlow", "PyTorch", "Pandas", "Scikit-Learn"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Data Engineer", "skills": ["Python", "SQL", "Apache Spark", "Hadoop", "Airflow", "ETL", "AWS", "Snowflake"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Machine Learning Engineer", "skills": ["Python", "Deep Learning", "TensorFlow", "PyTorch", "Computer Vision", "NLP", "C++"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "DevOps Engineer", "skills": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux", "Jenkins", "Ansible"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "UI/UX Designer", "skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Adobe XD", "HTML/CSS", "Sketch"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Product Manager", "skills": ["Product Management", "Agile", "Scrum", "Jira", "Data Analysis", "Roadmapping", "A/B Testing"], "prefixes": ["Associate", "Mid-Level", "Senior", "Lead"]},
    {"role": "Cybersecurity Analyst", "skills": ["Networking", "Python", "Linux", "Penetration Testing", "SIEM", "Security", "Firewalls"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Android Developer", "skills": ["Kotlin", "Android Studio", "Jetpack Compose", "Java", "Mobile Development", "Firebase"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "iOS Developer", "skills": ["Swift", "iOS", "SwiftUI", "Objective-C", "Mobile Development", "CoreData"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "QA Automation Engineer", "skills": ["Selenium", "Python", "Java", "Test Automation", "Cypress", "Appium", "JIRA"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "Business Analyst", "skills": ["Business Analysis", "Requirements Gathering", "SQL", "Excel", "Agile", "UML", "PowerBI"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]},
    {"role": "HR Manager", "skills": ["Talent Acquisition", "Onboarding", "Performance Management", "HR Policy", "Screening", "Interviewing"], "prefixes": ["Junior", "Mid-Level", "Senior", "Lead"]}
]

locations = ["Bengaluru, Karnataka, India", "Mumbai, Maharashtra, India", "Pune, Maharashtra, India", "Hyderabad, Telangana, India", "Delhi, India", "Chennai, Tamil Nadu, India", "Noida, Uttar Pradesh, India", "Gurgaon, Haryana, India", "Kolkata, West Bengal, India", "Remote"]

def generate_resume(idx):
    first_name = random.choice(names_first)
    last_name = random.choice(names_last)
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@email.com"
    phone = f"+91-9{random.randint(100000000, 999999999)}"
    
    role_info = random.choice(roles)
    prefix = random.choice(role_info["prefixes"])
    full_role = f"{prefix} {role_info['role']}" if prefix != "Mid-Level" else role_info['role']
    
    location = random.choice(locations)
    
    # Pick random subset of skills
    num_skills = random.randint(4, min(8, len(role_info["skills"])))
    selected_skills = random.sample(role_info["skills"], num_skills)
    # Add a few general skills
    general_skills = ["Git", "Postman", "Agile", "Jira", "Problem Solving"]
    selected_skills.extend(random.sample(general_skills, random.randint(1, 3)))
    random.shuffle(selected_skills)
    skills_str = ", ".join(selected_skills)
    
    years_exp = random.randint(1, 12)
    
    companies = ["Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra", "Cognizant", "Accenture", "IBM", "Capgemini", "Amazon", "Microsoft", "Google", "Startup Inc", "TechCorp", "Innovatech"]
    company = random.choice(companies)
    
    template = f"""{first_name.upper()} {last_name.upper()}
{full_role}
Email: {email} | Phone: {phone}
LinkedIn: linkedin.com/in/{first_name.lower()}{last_name.lower()} | GitHub: github.com/{first_name.lower()}{last_name.lower()}
Location: {location}

-------------------------------------------------------------------
SUMMARY
-------------------------------------------------------------------
Motivated and skilled {full_role} with {years_exp} years of experience in the industry.
Passionate about solving complex problems and delivering high-quality results.
Proven track record of success at {company} and in collaborative team environments.
Always eager to learn new technologies and improve existing skills.

-------------------------------------------------------------------
SKILLS
-------------------------------------------------------------------
Core Competencies: {skills_str}
Soft Skills: Communication, Teamwork, Time Management, Critical Thinking

-------------------------------------------------------------------
WORK EXPERIENCE
-------------------------------------------------------------------
{full_role} | {company}, {location.split(',')[0]}
Jan {2024 - min(years_exp, 4)} – Present
- Led the development and deployment of key features using {selected_skills[0]} and {selected_skills[1]}.
- Collaborated with cross-functional teams to define, design, and ship new capabilities.
- Improved system efficiency and reduced performance bottlenecks by 20%.

{role_info['role']} | Previous Company, {location.split(',')[0]}
Jun {2024 - years_exp} - Dec {2024 - min(years_exp, 4) - 1}
- Assisted in the design and implementation of core modules.
- Handled day-to-day operations and maintenance using {selected_skills[2] if len(selected_skills) > 2 else selected_skills[0]}.
- Participated in daily stand-ups and agile planning sessions.

-------------------------------------------------------------------
EDUCATION
-------------------------------------------------------------------
B.Tech / B.E. / Degree
XYZ University, India
Graduated: {2024 - years_exp - 1} | CGPA: {round(random.uniform(7.0, 9.8), 1)}/10

-------------------------------------------------------------------
PROJECTS
-------------------------------------------------------------------
Project Alpha
- Developed a comprehensive system leveraging {selected_skills[0]} to solve specific business needs.
- Ensured 99.9% uptime and robust scalability.

-------------------------------------------------------------------
CERTIFICATIONS
-------------------------------------------------------------------
- Certified Professional in {role_info['role']} (2022)
- Advanced Training in {selected_skills[0]}
"""
    filename = f"{idx:02d}_{first_name}_{last_name}_{role_info['role'].replace('/', '_').replace(' ', '_')}.txt"
    filepath = os.path.join(resumes_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)
    return filename, first_name, last_name, full_role

if __name__ == "__main__":
    generated = []
    for i in range(start_idx, 101):
        filename, fname, lname, role = generate_resume(i)
        generated.append((filename, fname, lname, role))
        
    print(f"Generated {len(generated)} new resumes.")
    
    # Update README
    readme_path = os.path.join(resumes_dir, "README.md")
    try:
        with open(readme_path, 'a', encoding='utf-8') as f:
            for idx, (filename, fname, lname, role) in enumerate(generated, start=start_idx):
                f.write(f"| {idx:02d} | {filename} | {fname} {lname} | {role} | Variable |\n")
        print("Appended to README.md")
    except Exception as e:
        print("Failed to update README:", e)
