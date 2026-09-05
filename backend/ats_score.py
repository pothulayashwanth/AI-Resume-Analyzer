from pathlib import Path
import re



BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_FILE = BASE_DIR / "data" / "resume.pdf"
JD_FILE = BASE_DIR / "data" / "jd.txt"


def extract_pdf_text(pdf_path):
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def calculate_keyword_score(resume_text, jd_text):
    resume_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", resume_text.lower()))
    jd_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", jd_text.lower()))

    
    stop_words = {
        "the", "and", "for", "with", "this", "that", "from",
        "are", "you", "your", "our", "will", "have", "has",
        "into", "about", "their", "they", "who", "what",
        "job", "work", "working", "looking"
    }

    jd_words -= stop_words

    if not jd_words:
        return 0

    matched_words = resume_words & jd_words

    return round((len(matched_words) / len(jd_words)) * 100, 2)


def calculate_section_score(resume_text):
    sections = {
        "education": ["education", "b.tech", "bachelor"],
        "experience": ["experience", "internship", "intern"],
        "projects": ["projects", "project"],
        "skills": ["skills", "technical skills"],
        "certifications": ["certification", "certifications"],
    }

    score = 0

    for keywords in sections.values():
        if any(keyword in resume_text for keyword in keywords):
            score += 20

    return score



resume_text = extract_pdf_text(RESUME_FILE)


jd_text = JD_FILE.read_text(encoding="utf-8")


resume_clean = clean_text(resume_text)
jd_clean = clean_text(jd_text)



keyword_score = calculate_keyword_score(resume_clean, jd_clean)
section_score = calculate_section_score(resume_clean)



ats_score = round(
    (keyword_score * 0.70) +
    (section_score * 0.30),
    2
)


print("\n========== ATS RESUME ANALYZER ==========\n")

print(f"Keyword Match Score : {keyword_score}%")
print(f"Resume Structure Score : {section_score}%")

print("-----------------------------------------")

print(f"FINAL ATS SCORE : {ats_score}%")

print("\n=========================================\n")



print("RECOMMENDATIONS:\n")

if keyword_score < 70:
    print("• Add more relevant keywords from the job description.")

if section_score < 80:
    print("• Improve resume sections such as Education, Experience, Projects, Skills and Certifications.")

if ats_score >= 80:
    print("• Your resume has a strong ATS match for this job.")

elif ats_score >= 60:
    print("• Your resume has a moderate ATS match. Add missing keywords and improve relevant sections.")

else:
    print("• Your resume needs significant optimization for this job.")