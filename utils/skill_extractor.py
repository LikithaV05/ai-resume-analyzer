# Simple skill list (you can expand later)
SKILLS_DB = [
    "python",
    "java",
    "sql",
    "machine learning",
    "data analysis",
    "nlp",
    "react",
    "spring boot",
    "docker",
    "aws",
    "git"
]

def extract_skills(text):
    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills
