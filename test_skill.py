from nlp_engine.pdf_parser import extract_text_from_pdf
from nlp_engine.skill_extractor import extract_skills

pdf_path = "media/resumes/vivek_resume_1.pdf"

text = extract_text_from_pdf(pdf_path)

skills = extract_skills(text)

print("Resume Skills:")

for skill in skills:
    print("-", skill)