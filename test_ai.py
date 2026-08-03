from nlp_engine.pdf_parser import extract_text_from_pdf
from nlp_engine.matcher import calculate_match

job_description = """
Python
Django
REST API
MySQL
Git
Docker
"""

pdf_path = "media/resumes/vivek_resume_1.pdf"

resume_text = extract_text_from_pdf(pdf_path)

score = calculate_match(
    job_description,
    resume_text
)

print("AI Match Score:", score, "%")