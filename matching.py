
import csv


def load_jobs(path="data/jobs.csv"):
    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def match_jobs(user_skills, jobs):
    user_set = {skill.strip().lower() for skill in user_skills}

    results = []

    for job in jobs:
        required = {
            skill.strip().lower()
            for skill in job["required_skills"].split(";")
            if skill.strip()
        }

        matched = user_set.intersection(required)

        score = round(100 * len(matched) / len(required)) if required else 0

        results.append({
            "job_title": job["job_title"],
            "match_score": score,
            "matched_skills": sorted(matched),
        })

    return sorted(
        results,
        key=lambda item: item["match_score"],
        reverse=True,
    )


if __name__ == "__main__":
    jobs = load_jobs()
    my_skills = ["Python", "SQL", "Pandas", "Git"]

    results = match_jobs(my_skills, jobs)

    for job in results:
        print(
            f"{job['job_title']}: {job['match_score']}% "
            f"| Matched skills: {', '.join(job['matched_skills'])}"
        )
