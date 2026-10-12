
RESOURCE_MAP = {
    "python": {
        "activity": "Learn Python fundamentals and practice functions, lists, and dictionaries.",
        "project": "Build a data-cleaning script.",
        "resource": "https://www.python.org/about/gettingstarted/",
    },
    "sql": {
        "activity": "Practice SELECT, JOIN, GROUP BY, and subqueries.",
        "project": "Create a database and analyze its records.",
        "resource": "https://www.w3schools.com/sql/",
    },
    "statistics": {
        "activity": "Learn averages, distributions, and basic hypothesis testing.",
        "project": "Analyze a dataset and explain your findings.",
        "resource": "https://www.khanacademy.org/math/statistics-probability",
    },
    "power bi": {
        "activity": "Learn data modeling and dashboard visualizations.",
        "project": "Build an interactive reporting dashboard.",
        "resource": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
    },
    "excel": {
        "activity": "Practice formulas, lookups, and pivot tables.",
        "project": "Create a spreadsheet analysis report.",
        "resource": "https://support.microsoft.com/en-us/excel",
    },
    "machine learning": {
        "activity": "Learn model training, evaluation, and data preparation.",
        "project": "Train and evaluate a simple prediction model.",
        "resource": "https://www.kaggle.com/learn/intro-to-machine-learning",
    },
    "pandas": {
        "activity": "Practice filtering, cleaning, and grouping data.",
        "project": "Analyze a CSV dataset using Pandas.",
        "resource": "https://pandas.pydata.org/docs/getting_started/",
    },
    "git": {
        "activity": "Learn commits, branches, and version control.",
        "project": "Track a Python project using Git.",
        "resource": "https://git-scm.com/doc",
    },
}


def generate_roadmap(missing_skills):
    roadmap = []

    for skill in missing_skills:
        details = RESOURCE_MAP.get(
            skill.strip().lower(),
            {
                "activity": f"Learn the fundamentals of {skill}.",
                "project": f"Build a small project using {skill}.",
                "resource": "https://www.google.com/search?q="
                + skill.replace(" ", "+")
                + "+tutorial",
            },
        )

        roadmap.append({
            "skill": skill,
            **details,
        })

    return roadmap


if __name__ == "__main__":
    for item in generate_roadmap(["Excel", "Power BI", "Statistics"]):
        print(f"\nSkill: {item['skill']}")
        print(f"Activity: {item['activity']}")
        print(f"Project: {item['project']}")
        print(f"Resource: {item['resource']}")
