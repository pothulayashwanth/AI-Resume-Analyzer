from pathlib import Path
import re
from pypdf import PdfReader


# ==============================
# PROJECT PATHS
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_FILE = BASE_DIR / "data" / "resume.pdf"
JD_FILE = BASE_DIR / "data" / "jd.txt"


# ==============================
# SKILLS DATABASE
# ==============================

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


# ==============================
# RESUME TEXT EXTRACTION
# ==============================

def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ==============================
# SKILL DETECTION
# ==============================

def find_skills(text):
    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return found


# ==============================
# SKILL MATCHING
# ==============================

def calculate_match(resume_skills, jd_skills):

    if not jd_skills:
        return 0

    matched = set(resume_skills) & set(jd_skills)

    score = (len(matched) / len(set(jd_skills))) * 100

    return round(score, 2)


# ==============================
# KEYWORD SCORE
# ==============================

def calculate_keyword_score(resume_text, jd_text):

    resume_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b",
            resume_text.lower()
        )
    )

    jd_words = set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b",
            jd_text.lower()
        )
    )

    stop_words = {
        "the", "and", "for", "with", "this", "that",
        "from", "are", "you", "your", "our", "will",
        "have", "has", "into", "about", "their",
        "they", "who", "what", "job", "work",
        "working", "looking"
    }

    jd_words -= stop_words

    if not jd_words:
        return 0

    matched_words = resume_words & jd_words

    return round(
        (len(matched_words) / len(jd_words)) * 100,
        2
    )


# ==============================
# RESUME STRUCTURE SCORE
# ==============================

def calculate_section_score(resume_text):

    sections = {
        "education": [
            "education",
            "b.tech",
            "bachelor"
        ],

        "experience": [
            "experience",
            "internship",
            "intern"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "certifications": [
            "certification",
            "certifications"
        ]
    }

    score = 0

    for keywords in sections.values():

        if any(keyword in resume_text for keyword in keywords):
            score += 20

    return score


# ==============================
# RECOMMENDATIONS
# ==============================

def generate_recommendations(missing_skills, ats_score):

    recommendations = []

    if missing_skills:

        recommendations.append(
            "Consider adding these job-relevant skills "
            "if you genuinely have knowledge or experience: "
            + ", ".join(missing_skills)
        )

    if "Data Structures" in missing_skills:

        recommendations.append(
            "If you have practiced Data Structures, "
            "mention relevant problems, coursework, "
            "or projects in your resume."
        )

    if "Algorithms" in missing_skills:

        recommendations.append(
            "If you have algorithm knowledge, highlight "
            "your DSA practice or algorithm-based projects."
        )

    if "APIs" in missing_skills:

        recommendations.append(
            "If you have worked with APIs, mention API "
            "integration or API development in relevant projects."
        )

    if ats_score < 70:

        recommendations.append(
            "Improve keyword alignment by naturally using "
            "relevant job-description terminology where it "
            "truthfully applies."
        )

    else:

        recommendations.append(
            "Your resume has good ATS alignment. Continue "
            "tailoring keywords and achievements to each job."
        )

    recommendations.append(
        "Do not add skills you do not actually know "
        "just to increase your ATS score."
    )

    return recommendations


# ==============================
# MAIN ANALYZER
# ==============================

def analyze_resume():

    print("\n")
    print("==========================================")
    print("        🤖 AI RESUME ANALYZER")
    print("==========================================")

    # Resume extraction
    resume_text = extract_pdf_text(RESUME_FILE)

    # Job description
    jd_text = JD_FILE.read_text(
        encoding="utf-8"
    )

    # Find skills
    resume_skills = find_skills(resume_text)

    jd_skills = find_skills(jd_text)

    # Matching
    matched_skills = sorted(
        set(resume_skills) &
        set(jd_skills)
    )

    missing_skills = sorted(
        set(jd_skills) -
        set(resume_skills)
    )

    skill_match_score = calculate_match(
        resume_skills,
        jd_skills
    )

    # Keyword score
    keyword_score = calculate_keyword_score(
        resume_text,
        jd_text
    )

    # Structure score
    section_score = calculate_section_score(
        resume_text.lower()
    )

    # Final ATS score
    ats_score = round(
        (keyword_score * 0.70) +
        (section_score * 0.30),
        2
    )

    # Recommendations
    recommendations = generate_recommendations(
        missing_skills,
        ats_score
    )

    # ==============================
    # DISPLAY RESULTS
    # ==============================

    print("\n📄 RESUME ANALYSIS")
    print("------------------------------------------")

    print(
        f"Resume Skills Found : {len(resume_skills)}"
    )

    print(
        f"JD Skills Found     : {len(jd_skills)}"
    )

    print("\n✅ MATCHED SKILLS")

    for skill in matched_skills:
        print(f"   ✓ {skill}")

    print("\n❌ MISSING SKILLS")

    if missing_skills:

        for skill in missing_skills:
            print(f"   ✗ {skill}")

    else:

        print("   No major missing skills!")

    print("\n📊 SCORES")
    print("------------------------------------------")

    print(
        f"Skill Match Score : {skill_match_score}%"
    )

    print(
        f"Keyword Score     : {keyword_score}%"
    )

    print(
        f"Structure Score   : {section_score}%"
    )

    print(
        f"🔥 FINAL ATS SCORE : {ats_score}%"
    )

    print("\n💡 RECOMMENDATIONS")
    print("------------------------------------------")

    for i, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print(
            f"{i}. {recommendation}"
        )

    print("\n==========================================")
    print("        ANALYSIS COMPLETE ✅")
    print("==========================================\n")


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    analyze_resume()