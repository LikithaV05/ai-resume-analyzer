def recommend_skills(missing_skills):

    recommendations = {}

    for skill in missing_skills:

        if skill == "nlp":
            recommendations[skill] = "Learn spaCy or HuggingFace basics."

        elif skill == "docker":
            recommendations[skill] = "Understand containerization and deployment."

        elif skill == "aws":
            recommendations[skill] = "Start with EC2 and S3 fundamentals."

        else:
            recommendations[skill] = "Build beginner projects to strengthen this skill."

    return recommendations

