import re

# List of skills the system can detect
SKILLS = [
    "Python",
    "Java",
    "Django",
    "Flask",
    "FastAPI",
    "Spring",
    "Spring Boot",
    "REST API",
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "MongoDB",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Bootstrap",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "OpenCV"
]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:

        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):

            found_skills.append(skill)

    return found_skills