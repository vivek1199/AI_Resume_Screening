def analyze_resume(job_skills, resume_skills):

    job = {
        skill.strip().lower()
        for skill in job_skills.split(",")
        if skill.strip()
    }

    resume = {
        skill.strip().lower()
        for skill in resume_skills
    }

    matched = sorted(job.intersection(resume))
    missing = sorted(job.difference(resume))

    if len(job) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job)) * 100, 2)

    if score >= 80:
        recommendation = "Highly Recommended"
    elif score >= 60:
        recommendation = "Recommended"
    else:
        recommendation = "Not Recommended"

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "recommendation": recommendation,
    }