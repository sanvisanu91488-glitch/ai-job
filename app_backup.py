
import streamlit as st

from src.matching import load_jobs, match_jobs
from src.skill_gap import analyze_skill_gap
from src.roadmap import generate_roadmap
from src.resume_parser import (
    extract_resume_text,
    extract_known_skills,
)


# =====================================
# 1. PAGE CONFIGURATION
# =====================================
st.set_page_config(
    page_title="InclusiveCareer AI",
    page_icon="🎯",
    layout="wide",
)

# =====================================
# 2. HEADER
# =====================================
st.title("🎯 InclusiveCareer AI")
st.subheader("Skills Over Barriers, Opportunities for Everyone.")

st.write(
    "Discover career opportunities based on your skills, "
    "identify skills to develop, and build a personalized learning plan."
)

st.divider()


# =====================================
# 3. AVAILABLE SKILLS
# =====================================
known_skills = [
    "Python",
    "SQL",
    "Excel",
    "Pandas",
    "Statistics",
    "Power BI",
    "Machine Learning",
    "NumPy",
    "Git",
    "APIs",
    "Testing",
    "Communication",
]


# =====================================
# 4. LOAD SAMPLE JOB DATA
# =====================================
try:
    jobs = load_jobs("data/jobs.csv")

    if not jobs:
        st.error("No jobs found. Please add records to data/jobs.csv.")
        st.stop()

except Exception as exc:
    st.error("Unable to load the job dataset.")
    st.code(str(exc))
    st.stop()


# =====================================
# 5. RESUME UPLOAD
# =====================================
st.header("1. Build Your Career Profile")

st.write(
    "Upload a PDF resume to detect listed skills, "
    "or select your skills manually."
)

resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

detected_skills = []

if resume is not None:
    try:
        resume_text = extract_resume_text(resume.getvalue())

        detected_skills = extract_known_skills(
            resume_text,
            known_skills,
        )

        if detected_skills:
            st.success("Skills detected from your resume.")
            st.write(", ".join(detected_skills))
        else:
            st.warning(
                "No known skills were detected. "
                "Please select your skills manually."
            )

    except Exception as exc:
        st.error(
            "Could not read this PDF. Try a text-based PDF "
            "or select your skills manually."
        )
        st.caption(str(exc))


# =====================================
# 6. CONFIRM SKILLS
# =====================================
user_skills = st.multiselect(
    "Confirm or select your skills",
    options=known_skills,
    default=[
        skill for skill in detected_skills
        if skill in known_skills
    ],
    help="Review the detected skills and correct them if needed.",
)


# =====================================
# 7. SELECT CAREER GOAL
# =====================================
st.header("2. Choose Your Career Goal")

job_titles = [
    job["job_title"]
    for job in jobs
    if job.get("job_title")
]

if not job_titles:
    st.error("No job titles are available in the dataset.")
    st.stop()

target_role = st.selectbox(
    "Which career are you interested in?",
    options=job_titles,
)


# =====================================
# 8. ANALYZE CAREER PROFILE
# =====================================
if st.button("Analyze My Career Profile", type="primary"):

    if not user_skills:
        st.warning("Please select at least one skill.")
        st.stop()

    # ---------------------------------
    # Job recommendations
    # ---------------------------------
    results = match_jobs(user_skills, jobs)

    st.divider()
    st.header("3. Recommended Career Roles")

    st.caption(
        "The match score represents the proportion of listed job "
        "skills that match your selected skills. It is not a hiring "
        "probability or a guarantee of eligibility."
    )

    st.dataframe(
        [
            {
                "Job Role": result["job_title"],
                "Skill Match (%)": result["match_score"],
                "Matched Skills": ", ".join(
                    result.get("matched_skills", [])
                ),
            }
            for result in results
        ],
        use_container_width=True,
        hide_index=True,
    )

    # ---------------------------------
    # Find selected job
    # ---------------------------------
    selected_job = next(
        (
            job for job in jobs
            if job.get("job_title") == target_role
        ),
        None,
    )

    if selected_job is None:
        st.error("The selected career could not be found.")
        st.stop()

    required_skills = [
        skill.strip()
        for skill in selected_job.get(
            "required_skills", ""
        ).split(";")
        if skill.strip()
    ]

    # ---------------------------------
    # Skill-gap analysis
    # ---------------------------------
    gap = analyze_skill_gap(
        user_skills,
        required_skills,
    )

    st.divider()
    st.header(f"4. Skill Gap Analysis: {target_role}")

    st.metric(
        "Required-Skill Coverage",
        f"{gap['coverage_score']}%",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills You Have")

        if gap["matched_skills"]:
            for skill in gap["matched_skills"]:
                st.write(f"• {skill}")
        else:
            st.write("No listed skills matched.")

    with col2:
        st.subheader("📚 Skills to Develop")

        if gap["missing_skills"]:
            for skill in gap["missing_skills"]:
                st.write(f"• {skill}")
        else:
            st.success("No listed skill gaps for this role!")

    # ---------------------------------
    # Personalized learning roadmap
    # ---------------------------------
    st.divider()
    st.header("5. Your Personalized Learning Roadmap")

    roadmap = generate_roadmap(gap["missing_skills"])

    if roadmap:
        for number, item in enumerate(roadmap, start=1):
            with st.expander(
                f"Step {number}: Learn {item['skill']}",
                expanded=True,
            ):
                st.write("**Learning activity:**")
                st.write(item["activity"])

                st.write("**Practical project:**")
                st.write(item["project"])

                resource_url = item.get("resource")

                if resource_url:
                    st.link_button(
                        "Open Learning Resource",
                        resource_url,
                    )
                else:
                    st.caption(
                        "Add a learning resource in src/roadmap.py "
                        "for this skill."
                    )

    else:
        st.success(
            "You match all the listed skills for this role. "
            "Consider building a portfolio project to demonstrate "
            "your abilities."
        )

    # ---------------------------------
    # Transparency and inclusion
    # ---------------------------------
    st.divider()
    st.header("6. About Your Recommendations")

    st.info(
        "This prototype uses sample job data, selected skills, "
        "and keyword-based resume detection. Review detected skills "
        "carefully. The system may miss relevant experience or skills "
        "expressed differently. Matching scores are informational "
        "and do not guarantee employment."
    )


# =====================================
# 9. FOOTER
# =====================================
st.divider()

st.caption(
    "InclusiveCareer AI | Skills Over Barriers, Opportunities for Everyone."
)
