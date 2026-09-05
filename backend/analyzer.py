from pathlib import Path
import re
from collections import Counter
from pypdf import PdfReader

# Canonical skills and common aliases.
SKILL_ALIASES = {
    "Python":["python","python3","python 3"],
    "Java":["java"],
    "C":["c programming","c language"],
    "C++":["c++","cpp"],
    "C#":["c#","c sharp","csharp"],
    "JavaScript":["javascript","js","ecmascript"],
    "TypeScript":["typescript","ts"],
    "HTML":["html","html5"],
    "CSS":["css","css3"],
    "React":["react","reactjs","react.js"],
    "Angular":["angular","angularjs"],
    "Vue":["vue","vue.js","vuejs"],
    "Node.js":["node.js","nodejs","node"],
    "Express":["express","express.js","expressjs"],
    "Django":["django"],
    "Flask":["flask"],
    "FastAPI":["fastapi","fast api"],
    "Spring":["spring boot","spring"],
    "SQL":["sql","structured query language"],
    "MySQL":["mysql"],
    "PostgreSQL":["postgresql","postgres"],
    "MongoDB":["mongodb","mongo db"],
    "SQLite":["sqlite"],
    "Redis":["redis"],
    "Machine Learning":["machine learning","machine-learning","ml"],
    "Deep Learning":["deep learning","deep-learning","dl"],
    "Artificial Intelligence":["artificial intelligence","artificial-intelligence","ai"],
    "NLP":["natural language processing","nlp"],
    "Computer Vision":["computer vision","cv"],
    "scikit-learn":["scikit-learn","sklearn","scikit learn"],
    "Pandas":["pandas"],
    "NumPy":["numpy","num py"],
    "TensorFlow":["tensorflow","tensor flow"],
    "PyTorch":["pytorch","py torch"],
    "Data Analysis":["data analysis","data analytics"],
    "Data Science":["data science","data-science"],
    "Statistics":["statistics","statistical analysis"],
    "Data Structures":["data structures","data structure","dsa"],
    "Algorithms":["algorithms","algorithm"],
    "OOP":["object oriented programming","object-oriented programming","oop"],
    "DBMS":["dbms","database management systems"],
    "Git":["git"],
    "GitHub":["github","github.com"],
    "GitLab":["gitlab"],
    "REST APIs":["rest api","rest apis","restful api","restful apis"],
    "APIs":["api","apis","application programming interface"],
    "AWS":["aws","amazon web services"],
    "Azure":["azure","microsoft azure"],
    "GCP":["gcp","google cloud","google cloud platform"],
    "Docker":["docker","containerization"],
    "Kubernetes":["kubernetes","k8s"],
    "Linux":["linux","ubuntu"],
    "CI/CD":["ci/cd","cicd","continuous integration","continuous deployment"],
    "Jenkins":["jenkins"],
    "Postman":["postman"],
    "VS Code":["vs code","visual studio code"],
    "Figma":["figma"],
    "Power BI":["power bi","powerbi"],
    "Excel":["excel","microsoft excel"],
}

SHORT_ALIASES = {"js","ts","ml","dl","ai","cv","dsa","node","api","apis"}
STOP_WORDS = {
    "the","and","for","with","this","that","from","are","you","your","our",
    "will","have","has","into","about","their","they","who","what","job",
    "work","working","looking","role","candidate","team","using","use","used",
    "years","year","ability","strong","good","excellent","preferred","required",
    "requirements","responsibilities","experience","including","etc","such",
    "within","across","based","related","skills","skill","knowledge"
}
ACTION_VERBS = [
    "developed","designed","built","implemented","created","engineered",
    "optimized","automated","integrated","deployed","analyzed","managed",
    "led","improved","tested","configured","maintained","collaborated",
    "architected","delivered","launched","migrated","refactored",
    "streamlined","reduced","increased","achieved","resolved","debugged",
    "trained","evaluated","researched","prototyped"
]
SECTION_ALIASES = {
    "education":["education","academic background","academic qualifications"],
    "experience":["experience","work experience","professional experience","employment","internship","internships"],
    "projects":["projects","project experience","academic projects"],
    "skills":["skills","technical skills","technical expertise","core skills","technologies"],
    "certifications":["certification","certifications","courses","training"],
    "summary":["summary","professional summary","profile","objective","career objective"],
}
JD_PHRASES = [
    "software development","web development","full stack","frontend development",
    "backend development","data analysis","data analytics","machine learning",
    "deep learning","natural language processing","computer vision",
    "problem solving","object oriented programming","database management",
    "api development","rest api","cloud computing","version control",
    "unit testing","agile","scrum","communication","leadership","teamwork"
]
REQUIRED_MARKERS = ["required","must have","must-have","mandatory","essential","you will need","need to have"]
PREFERRED_MARKERS = ["preferred","nice to have","nice-to-have","plus","bonus","good to have"]

def normalize_text(text):
    text = (text or "").replace("\u00a0"," ").replace("\u2013","-").replace("\u2014","-")
    text = re.sub(r"[ \t]+"," ",text)
    text = re.sub(r"\n{3,}","\n\n",text)
    return text.strip()

def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    return normalize_text("\n".join(parts))

def words(text):
    return re.findall(r"[a-z0-9][a-z0-9+#./'-]*", (text or "").lower())

def contains_term(text, term):
    text, term = (text or "").lower(), term.lower().strip()
    if not term:
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text))

def find_skills(text):
    text = normalize_text(text)
    return sorted([
        skill for skill, aliases in SKILL_ALIASES.items()
        if any(contains_term(text, a) for a in aliases)
    ])

def split_jd_skill_priority(jd):
    required, preferred = set(), set()
    skills = find_skills(jd)
    for line in [x.strip() for x in normalize_text(jd).splitlines() if x.strip()]:
        low = line.lower()
        for skill in skills:
            if any(contains_term(low, a) for a in SKILL_ALIASES[skill]):
                if any(m in low for m in REQUIRED_MARKERS):
                    required.add(skill)
                elif any(m in low for m in PREFERRED_MARKERS):
                    preferred.add(skill)
    return required, preferred

def calculate_skill_match(resume_skills, jd_skills, required_skills=None, preferred_skills=None):
    jd = set(jd_skills)
    resume = set(resume_skills)
    if not jd:
        return 0.0
    required = set(required_skills or [])
    preferred = set(preferred_skills or [])
    total = matched = 0.0
    for skill in jd:
        weight = 2.0 if skill in required else 0.75 if skill in preferred else 1.0
        total += weight
        if skill in resume:
            matched += weight
    return round(matched / total * 100, 2) if total else 0.0

def extract_jd_keywords(jd):
    text = normalize_text(jd).lower()
    counter = Counter()
    detected = set(find_skills(text))
    for skill in detected:
        counter[skill] += 3
    for phrase in JD_PHRASES:
        if contains_term(text, phrase):
            counter[phrase] += 2
    for token in words(text):
        if len(token) >= 4 and token not in STOP_WORDS and not token.isdigit():
            counter[token] += 1
    return [(k,v) for k,v in counter.items()
            if v >= 2 or k in detected or k in JD_PHRASES]

def calculate_keyword_score(resume_text, jd_text):
    keywords = extract_jd_keywords(jd_text)
    if not keywords:
        return 0.0
    total = sum(weight for _,weight in keywords)
    matched = sum(weight for keyword,weight in keywords
                  if contains_term(resume_text, keyword))
    return round(matched / total * 100, 2) if total else 0.0

def detect_sections(text):
    lines = [
        re.sub(r"[^a-zA-Z0-9+#/& -]","",line.lower()).strip()
        for line in normalize_text(text).splitlines()
    ]
    result = {}
    for section, aliases in SECTION_ALIASES.items():
        result[section] = any(
            len(line) <= 60 and any(
                line == a or line.startswith(a+" ") or line.endswith(" "+a)
                for a in aliases
            ) for line in lines
        )
    return result

def calculate_structure_score(text):
    s = detect_sections(text)
    low = normalize_text(text).lower()
    checks = {
        "summary":s["summary"], "education":s["education"],
        "experience":s["experience"], "projects":s["projects"],
        "skills":s["skills"], "certifications":s["certifications"],
        "LinkedIn":"linkedin.com" in low, "GitHub":"github.com" in low
    }
    weights = {"summary":.75,"education":1,"experience":1.5,"projects":1.25,
               "skills":1.5,"certifications":.75,"LinkedIn":.5,"GitHub":.5}
    total = sum(weights.values())
    return round(sum(weights[k] for k,v in checks.items() if v)/total*100,2)

def analyze_resume_quality(text):
    low = normalize_text(text).lower()
    sections = detect_sections(text)
    checks = {
        "Email": bool(re.search(r"[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}",text)),
        "Phone": bool(re.search(r"(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}",text)),
        "Education":sections["education"], "Experience":sections["experience"],
        "Projects":sections["projects"], "Skills":sections["skills"],
        "Certifications":sections["certifications"],
        "LinkedIn":"linkedin.com" in low, "GitHub":"github.com" in low
    }
    weights = {"Email":1.25,"Phone":1,"Education":1,"Experience":1.5,
               "Projects":1.25,"Skills":1.5,"Certifications":.5,
               "LinkedIn":.5,"GitHub":.5}
    total = sum(weights.values())
    score = round(sum(weights[k] for k,v in checks.items() if v)/total*100,2)
    return {"checks":checks,"quality_score":score}

def analyze_resume_content(text):
    low = normalize_text(text).lower()
    verbs = [v for v in ACTION_VERBS if contains_term(low,v)]
    patterns = [
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b\d+(?:\.\d+)?\s*\+",
        r"\b\d+(?:\.\d+)?\s*(?:users?|customers?|projects?|records?|students?|members?)\b",
        r"\b\d+(?:\.\d+)?\s*(?:ms|milliseconds|seconds?|minutes?|hours?|days?)\b",
        r"\b(?:increased|reduced|improved|saved|grew|boosted|cut)\s+(?:by\s+)?\d+(?:\.\d+)?\s*%"
    ]
    metrics = []
    for p in patterns:
        for match in re.findall(p,low):
            if match.strip() not in metrics:
                metrics.append(match.strip())
    count = len(words(text))
    action_score = min(len(verbs)/6,1)*30
    metric_score = min(len(metrics)/3,1)*35
    detail_score = min(count/450,1)*35
    score = round(min(action_score+metric_score+detail_score,100),2)
    suggestions = []
    if len(verbs) < 4:
        suggestions.append("Use stronger action verbs in project and experience bullets where accurate.")
    if not metrics:
        suggestions.append("Where truthful, quantify outcomes with users, accuracy, time saved, or percentage improvement.")
    if count < 150:
        suggestions.append("The extracted resume text is short; add meaningful project, experience, education, and achievement details.")
    if not suggestions:
        suggestions.append("Your resume contains a reasonable mix of action-oriented language and measurable information.")
    return {"action_verbs":verbs,"metrics":metrics,"content_score":score,"suggestions":suggestions}

def calculate_ats_score(keyword_score, skill_match_score, structure_score, quality_score):
    return round(keyword_score*.45 + skill_match_score*.30 + structure_score*.15 + quality_score*.10,2)

def calculate_overall_score(ats_score, skill_match_score, quality_score, content_score):
    return round(min(max(ats_score*.40 + skill_match_score*.25 + quality_score*.15 + content_score*.20,0),100),2)

def generate_priority_recommendations(missing_skills, ats_score, skill_match_score,
                                      quality_score, content_score, resume_content,
                                      jd_skills=None, required_skills=None):
    recs = []
    required = set(required_skills or [])
    missing_required = sorted(set(missing_skills) & required)
    if missing_required:
        recs.append({"priority":"HIGH","category":"Required Skills",
                      "message":"Required skills not detected in the resume: " +
                      ", ".join(missing_required) +
                      ". Add them only if you genuinely have the knowledge or experience."})
    elif missing_skills:
        recs.append({"priority":"MEDIUM","category":"Job Skills",
                      "message":"Job-relevant skills not detected: " +
                      ", ".join(missing_skills[:8]) +
                      ". Include them only when they truthfully reflect your experience."})
    if ats_score < 70:
        recs.append({"priority":"HIGH","category":"ATS",
                      "message":"Your ATS alignment is below 70%. Improve coverage of important job-specific terminology naturally in relevant skills, projects, and experience sections."})
    if skill_match_score < 70 and jd_skills:
        recs.append({"priority":"HIGH","category":"Job Match",
                      "message":"The detected skill alignment is below 70%. Highlight relevant experience you already have for this target role."})
    if content_score < 70:
        recs.append({"priority":"MEDIUM","category":"Content",
                      "message":"Strengthen project and experience bullets with specific actions, technologies used, and truthful outcomes."})
    if not resume_content["metrics"]:
        recs.append({"priority":"MEDIUM","category":"Achievements",
                      "message":"No clear measurable results were detected. Where truthful, add numbers such as accuracy, users, time saved, or percentage improvement."})
    if len(resume_content["action_verbs"]) < 4:
        recs.append({"priority":"MEDIUM","category":"Action Verbs",
                      "message":"Use stronger action-oriented wording where accurate, such as Developed, Implemented, Designed, Optimized, Automated, or Deployed."})
    if quality_score < 75:
        recs.append({"priority":"MEDIUM","category":"Resume Structure",
                      "message":"Some common resume sections or contact details were not detected. Review Education, Experience, Projects, Skills, and contact links."})
    if not recs:
        recs.append({"priority":"LOW","category":"Overall",
                      "message":"The resume shows good alignment with the supplied job description. Continue tailoring each application truthfully."})
    recs.append({"priority":"IMPORTANT","category":"Accuracy",
                  "message":"Never add a skill, technology, experience, certification, or achievement that you do not actually have."})
    return recs

def generate_recommendations(missing_skills, ats_score):
    recs = []
    if missing_skills:
        recs.append("Review missing job-relevant skills and include them only when they truthfully match your knowledge or experience: " + ", ".join(missing_skills))
    if ats_score < 70:
        recs.append("Improve ATS alignment by naturally using relevant job-description terminology where it truthfully applies.")
    recs.append("Do not add skills you do not actually know just to increase your ATS score.")
    return recs

def analyze_resume(resume_path, job_description):
    """
    Existing frontend-compatible API.
    No frontend changes are required.
    """
    if not resume_path:
        raise ValueError("Resume path is required.")
    if not job_description or not job_description.strip():
        raise ValueError("Job description is required.")

    resume_text = extract_pdf_text(resume_path)
    jd_text = normalize_text(job_description)

    if len(words(resume_text)) < 20:
        raise ValueError("Very little readable text was extracted from the resume. Please upload a text-based or OCR-readable PDF.")
    if len(words(jd_text)) < 10:
        raise ValueError("The job description is too short to produce a reliable comparison.")

    quality = analyze_resume_quality(resume_text)
    content = analyze_resume_content(resume_text)

    resume_skills = find_skills(resume_text)
    jd_skills = find_skills(jd_text)
    required, preferred = split_jd_skill_priority(jd_text)

    matched = sorted(set(resume_skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    skill_match = calculate_skill_match(
        resume_skills, jd_skills, required, preferred
    )
    keyword_score = calculate_keyword_score(resume_text, jd_text)
    structure_score = calculate_structure_score(resume_text)

    ats_score = calculate_ats_score(
        keyword_score, skill_match, structure_score, quality["quality_score"]
    )
    overall_score = calculate_overall_score(
        ats_score, skill_match, quality["quality_score"], content["content_score"]
    )

    priority = generate_priority_recommendations(
        missing, ats_score, skill_match, quality["quality_score"],
        content["content_score"], content, jd_skills, required
    )

    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "required_skills": sorted(required),
        "preferred_skills": sorted(preferred),
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match_score": skill_match,
        "keyword_score": keyword_score,
        "structure_score": structure_score,
        "ats_score": ats_score,
        "recommendations": generate_recommendations(missing, ats_score),
        "resume_quality": quality,
        "quality_score": quality["quality_score"],
        "resume_content": content,
        "content_score": content["content_score"],
        "overall_score": overall_score,
        "priority_recommendations": priority,
    }

if __name__ == "__main__":
    print("AI Resume Analyzer backend loaded successfully.")
