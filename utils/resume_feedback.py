def generate_feedback(match_score, missing_skills):

    feedback = []

    if match_score > 75:
        feedback.append("Strong alignment with job role.")
    elif match_score > 50:
        feedback.append("Moderate match. Improve missing skills.")
    else:
        feedback.append("Low match. Consider adding more relevant projects.")

    if len(missing_skills) > 3:
        feedback.append("Focus on learning core missing technologies.")

    if "aws" in missing_skills:
        feedback.append("Cloud exposure will strengthen your resume.")

    return feedback
