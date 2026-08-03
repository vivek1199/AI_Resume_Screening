from nlp_engine.matcher import calculate_match

job_description = """
Python
Django
REST API
MySQL
Git
Docker
"""

resume = """
Python
Django
Git
MySQL
"""

score = calculate_match(
    job_description,
    resume
)

print("Match Score:", score, "%")