
def normalize_skills(skills):
    return {
        skill.strip().lower()
        for skill in skills
        if skill.strip()
    }


def analyze_skill_gap(user_skills, required_skills):
    user_set = normalize_skills(user_skills)
    required_set = normalize_skills(required_skills)

    matched = sorted(user_set & required_set)
    missing = sorted(required_set - user_set)

    coverage = (
        round(100 * len(matched) / len(required_set))
        if required_set
        else 0
    )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage_score": coverage,
    }


if __name__ == "__main__":
    user_skills = ["Python", "SQL", "Pandas"]

    required_skills = [
        "Python", "SQL", "Pandas", "Excel", "Power BI"
    ]

    result = analyze_skill_gap(user_skills, required_skills)

    print("Skills you have:", result["matched_skills"])
    print("Skills to learn:", result["missing_skills"])
    print("Required-skill coverage:", str(result["coverage_score"]) + "%")
