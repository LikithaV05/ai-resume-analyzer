from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity
from utils.skill_gap import find_skill_gap

resume_path = r"C:\Users\Likitha\Downloads\Likitha Resume.pdf"

resume_text = extract_text_from_pdf(resume_path)

job_description = """
Looking for a Python developer with Machine Learning, NLP, AWS and Docker experience.
Strong knowledge of SQL and Data Analysis required.
"""

resume_skills = extract_skills(resume_text)
job_skills = extract_skills(job_description)

match_score = calculate_similarity(resume_text, job_description)

missing_skills = find_skill_gap(resume_skills, job_skills)

print("Resume Skills:", resume_skills)
print("Job Skills:", job_skills)
print("Match Score:", match_score, "%")
print("Missing Skills:", missing_skills)
