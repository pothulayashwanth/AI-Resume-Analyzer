import pymupdf
import re

pdf_path = "../data/resume.pdf"

document = pymupdf.open(pdf_path)
resume_text = ""
for page in document:
    resume_text +=page.get_text()
document.close()
email=re.search(r'[\w\.-]+@[\w\.-]+\.\w+',resume_text)
if email:
    print("Email:",email.group())
else:
    print("Email:Not found.")
phone = re.search(r'(\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}', resume_text)

if phone:
    print("Phone:", phone.group())
else:
    print("Phone: Not found")
skills = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
        "Go", "Rust", "Kotlin", "Swift", "PHP", "Ruby", "R", "MATLAB"
    ],

    "Web Development": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Next.js",
        "Node.js", "Express.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "REST API", "GraphQL"
    ],

    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle",
        "SQL Server", "Redis", "Cassandra", "SQLite", "Firebase"
    ],

    "AI & Machine Learning": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "TensorFlow", "PyTorch", "Keras",
        "scikit-learn", "Pandas", "NumPy", "OpenCV",
        "Matplotlib", "Seaborn", "Hugging Face", "Transformers"
    ],

    "Cloud & DevOps": [
        "AWS", "Microsoft Azure", "Google Cloud", "Docker",
        "Kubernetes", "Jenkins", "GitHub Actions", "Terraform",
        "Ansible", "Linux", "CI/CD"
    ],

    "Data & Analytics": [
        "Power BI", "Tableau", "Excel", "Apache Spark",
        "Hadoop", "Apache Airflow", "Data Analysis", "Data Visualization"
    ],

    "Tools & Version Control": [
        "Git", "GitHub", "GitLab", "Jira", "Postman",
        "VS Code", "IntelliJ IDEA"
    ],

    "Cybersecurity": [
        "Cybersecurity", "Network Security", "Ethical Hacking",
        "Penetration Testing", "Cryptography", "OWASP",
        "Kali Linux", "Wireshark", "Burp Suite"
    ]
}
found_skills = {}

for category, skill_list in skills.items():
    found = []

    for skill in skill_list:
        if skill.lower() in resume_text.lower():
            found.append(skill)

    if found:
        found_skills[category] = found

print("\nSkills Found:")

for category, skill_list in found_skills.items():
    print(f"\n{category}:")

    for skill in skill_list:
        print("-", skill)