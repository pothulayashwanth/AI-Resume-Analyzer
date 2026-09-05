def generate_recommendations(missing_skills, ats_score):
    recommendations = []

    if missing_skills:
        recommendations.append(
            "Consider adding these job-relevant skills to your resume "
            "if you genuinely have knowledge or experience with them: "
            + ", ".join(missing_skills)
        )

    if "Data Structures" in missing_skills:
        recommendations.append(
            "If you have practiced Data Structures, mention relevant "
            "problems, coursework, or projects in your resume."
        )

    if "Algorithms" in missing_skills:
        recommendations.append(
            "If you have algorithm knowledge, highlight your DSA practice "
            "or algorithm-based projects."
        )

    if "APIs" in missing_skills:
        recommendations.append(
            "If you have worked with APIs, mention API integration or "
            "API development in your relevant projects."
        )

    if ats_score < 70:
        recommendations.append(
            "Improve keyword alignment by naturally using relevant "
            "job-description terminology where it truthfully applies."
        )

    if ats_score >= 70:
        recommendations.append(
            "Your resume has good ATS alignment. Continue tailoring "
            "keywords and achievements to each job description."
        )

    recommendations.append(
        "Do not add skills you do not actually know just to increase "
        "your ATS score."
    )

    return recommendations


# Example test
if __name__ == "__main__":
    missing = ["APIs", "Algorithms", "Data Structures"]
    score = 60.51

    results = generate_recommendations(missing, score)

    print("\n========== RESUME RECOMMENDATIONS ==========\n")

    for i, recommendation in enumerate(results, start=1):
        print(f"{i}. {recommendation}")

    print("\n============================================")