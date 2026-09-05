import re
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_FILE = BASE_DIR / "data" / "resume.pdf"
JD_FILE = BASE_DIR / "data" / "jd.txt"


# Skills our analyzer can detect
SKILLS = [
    "Python",
    "Java",
    "C",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "SQL",
    "MySQL",
    "Machine Learning",
    "NLP",
    "scikit-learn",
    "Pandas",
    "NumPy",
    "Data Analysis",
    "Git",
    "GitHub",
    "VS Code",
    "Data Structures",
    "Algorithms",
    "APIs",
    "Django",
    "Flask",
    "Node.js",
    "Express",
    "MongoDB",
    "AWS",
    "Docker"
]


def extract_pdf_text(pdf_path):
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def normalize_text(text):
    return text.lower()


def find_skills(text):
    text = normalize_text(text)
    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found


def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = set(resume_skills) & set(jd_skills)

    score = (len(matched) / len(set(jd_skills))) * 100

    return round(score, 2)


# Extract resume text
resume_text = extract_pdf_text(RESUME_FILE)

# Read job description
jd_text = JD_FILE.read_text(encoding="utf-8")


# Find skills
resume_skills = find_skills(resume_text)
jd_skills = find_skills(jd_text)

# Find matched and missing skills
matched_skills = sorted(set(resume_skills) & set(jd_skills))
missing_skills = sorted(set(jd_skills) - set(resume_skills))

# Calculate score
match_score = calculate_match(resume_skills, jd_skills)


print("\n========== AI RESUME ANALYZER ==========\n")

print(f"Resume Skills Found: {len(resume_skills)}")
print(f"JD Skills Found: {len(jd_skills)}")

print("\nMatched Skills:")
if matched_skills:
    for skill in matched_skills:
        print(f"✓ {skill}")
else:
    print("No matching skills found.")

print("\nMissing Skills:")
if missing_skills:
    for skill in missing_skills:
        print(f"✗ {skill}")
else:
    print("No major missing skills found.")

print(f"\nResume Match Score: {match_score}%")

print("\n========================================")
