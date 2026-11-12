
from nlp_engine.matcher import calculate_match


def analyze_resume(job_skills, resume_skills, job_description="", resume_text=""):
    """Analyze a resume against a particular job."""

    job = {
        skill.strip().lower()
        for skill in job_skills.split(",")
        if skill.strip()
    }

    resume = {
        skill.strip().lower()
        for skill in resume_skills
        if skill.strip()
    }

    matched = sorted(job.intersection(resume))
    missing = sorted(job.difference(resume))

    skill_score = (
        (len(matched) / len(job)) * 100
        if job else 0
    )

    text_score = calculate_match(
        job_description,
        resume_text
    )

    # Combined score: 70% skills + 30% text similarity
    final_score = (skill_score * 0.70) + (text_score * 0.30)

    final_score = round(final_score, 2)

    if final_score >= 80:
        recommendation = "Highly Recommended"
    elif final_score >= 60:
        recommendation = "Recommended"
    else:
        recommendation = "Needs Review"

    return {
        "score": final_score,
        "skill_score": round(skill_score, 2),
        "text_score": round(text_score, 2),
        "matched": matched,
        "missing": missing,
        "recommendation": recommendation,
    }
