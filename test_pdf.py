from nlp_engine.pdf_parser import extract_text_from_pdf

pdf_path = "media/resumes/vivek_resume_1.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)