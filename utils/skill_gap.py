def find_skill_gap(resume_skills, job_skills):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    missing_skills = list(job_set - resume_set)

    return missing_skills
