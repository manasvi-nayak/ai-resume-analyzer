import re

def clean_text(text):
    return text.lower()

def extract_skills(text, skills_db):
    detected = []
    for skill in skills_db:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            detected.append(skill)
    return detected

def calculate_score(detected, required):
    match = len(set(detected) & set(required))
    total = len(required)
    return int((match / total) * 100)

def get_best_jobs(detected, jobs):
    results = {}
    for job, skills in jobs.items():
        score = calculate_score(detected, skills)
        results[job] = score
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

def get_missing_skills(detected, required):
    return list(set(required) - set(detected))