
import streamlit as st

from src.matching import load_jobs, match_jobs
from src.skill_gap import analyze_skill_gap
from src.roadmap import generate_roadmap
from src.resume_parser import extract_resume_text, extract_known_skills


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="InclusiveCareer AI",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# FRIENDLY, ACCESSIBLE DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Main application background */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background: #F7F8FC !important;
        color: #26324B !important;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Readable headings */
    h1, h2, h3, h4, h5, h6 {
        color: #33266F !important;
    }

    /* Normal text */
    p, li, label,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stWidgetLabel"] p {
        color: #26324B !important;
    }

    /* Captions and secondary text */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #596579 !important;
    }

    /* Welcome banner */
    .hero {
        background: linear-gradient(120deg, #E7EAFF, #F2E8FF);
        padding: 2rem;
        border-radius: 22px;
        border: 1px solid #D9D5FA;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: #33266F !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #403A60 !important;
        font-size: 1.05rem;
    }

    .section-heading {
        color: #33266F !important;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.3rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #DCDFF0 !important;
        padding: 1rem;
        border-radius: 15px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #46516A !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #33266F !important;
    }

    /* White career and skill cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border-color: #E0E3F0 !important;
        border-radius: 15px;
    }

    /* Resume uploader */
    [data-testid="stFileUploader"] {
        background: #FFFFFF !important;
        padding: 1rem;
        border-radius: 14px;
        border: 1px dashed #A8A0E8;
    }

    /* Select boxes and text inputs */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background: #FFFFFF !important;
        border-color: #C9CDE0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: #6558D9 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px;
        min-height: 3rem;
        font-weight: 600;
    }

    .stButton > button p,
    .stButton > button span {
        color: #FFFFFF !important;
    }

    .stButton > button:hover {
        background: #5145BD !important;
        color: #FFFFFF !important;
    }

    /* Learning links */
    .stLinkButton > a {
        background: #6558D9 !important;
        color: #FFFFFF !important;
        border-radius: 10px;
        border: none !important;
    }

    .stLinkButton > a p,
    .stLinkButton > a span {
        color: #FFFFFF !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #F0EEFF !important;
    }

    /* Header */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Progress bars */
    [data-testid="stProgressBar"] > div > div {
        background: #6558D9 !important;
    }

    /* Keep warning and success messages readable */
    [data-testid="stAlert"] p {
        color: #26324B !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# WELCOME HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🌈 InclusiveCareer AI</h1>
        <p><b>Skills Over Barriers, Opportunities for Everyone.</b></p>
        <p>
            Your skills matter. Discover career opportunities,
            understand what to learn next, and build your future
            one step at a time.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

feature1, feature2, feature3 = st.columns(3)

with feature1:
    st.markdown("### 🧭 Discover")
    st.caption("Explore careers that match your skills.")

with feature2:
    st.markdown("### 🪴 Grow")
    st.caption("Identify skills you can develop.")

with feature3:
    st.markdown("### 🚀 Take action")
    st.caption("Follow a personalized learning roadmap.")

st.divider()


# --------------------------------------------------
# KNOWN SKILLS
# --------------------------------------------------
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


# --------------------------------------------------
# LOAD JOB DATASET
# --------------------------------------------------
try:
    jobs = load_jobs("data/jobs.csv")

    if not jobs:
        st.error("No jobs were found in data/jobs.csv.")
        st.stop()

except Exception as exc:
    st.error("We couldn't load the job dataset.")
    st.caption("Check that data/jobs.csv exists and has the required columns.")
    st.code(str(exc))
    st.stop()


# --------------------------------------------------
# SECTION 1: CAREER PROFILE
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">💜 1. Build Your Career Profile</div>',
    unsafe_allow_html=True,
)

st.write(
    "Upload your resume or select your skills manually. "
    "You can review and correct detected skills."
)

resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
    help="Text-based PDF resumes are supported. Scanned PDFs may require OCR.",
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
            st.success("We found some skills in your resume!")
            st.write(", ".join(detected_skills))
        else:
            st.warning(
                "We couldn't detect any listed skills. "
                "Please select your skills manually."
            )

    except Exception as exc:
        st.error(
            "We couldn't read this PDF. Try a text-based PDF "
            "or select your skills manually."
        )
        st.caption(str(exc))

user_skills = st.multiselect(
    "Your skills",
    options=known_skills,
    default=[
        skill for skill in detected_skills
        if skill in known_skills
    ],
    help="Choose the skills you currently have.",
    placeholder="Choose your skills...",
)

st.divider()


# --------------------------------------------------
# SECTION 2: CAREER GOAL
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">🎯 2. Choose Your Career Goal</div>',
    unsafe_allow_html=True,
)

job_titles = [
    job["job_title"]
    for job in jobs
    if job.get("job_title")
]

if not job_titles:
    st.error("No career roles are available in the dataset.")
    st.stop()

target_role = st.selectbox(
    "Which career would you like to work toward?",
    options=job_titles,
)

st.caption(
    "You can explore all recommended roles after the analysis."
)

analyze_clicked = st.button(
    "✨ Analyze My Career Profile",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# SECTION 3–6: RESULTS
# --------------------------------------------------
if analyze_clicked:

    if not user_skills:
        st.warning(
            "Please select at least one skill before analyzing your profile."
        )
        st.stop()

    results = match_jobs(user_skills, jobs)

    selected_job = next(
        (
            job for job in jobs
            if job.get("job_title") == target_role
        ),
        None,
    )

    if selected_job is None:
        st.error("We couldn't find your selected career.")
        st.stop()

    required_skills = [
        skill.strip()
        for skill in selected_job.get("required_skills", "").split(";")
        if skill.strip()
    ]

    gap = analyze_skill_gap(user_skills, required_skills)

    # ----------------------------------------------
    # CAREER RECOMMENDATIONS
    # ----------------------------------------------
    st.divider()

    st.markdown(
        '<div class="section-heading">🌟 3. Career Recommendations</div>',
        unsafe_allow_html=True,
    )

    st.write("Here are the roles that best match your skills.")

    st.info(
        "Match scores show the percentage of listed job skills that "
        "match your selected skills. They are not hiring probabilities "
        "or guarantees of eligibility."
    )

    for result in results:

        with st.container(border=True):

            left, right = st.columns([3, 1])

            with left:
                st.subheader("💼 " + result["job_title"])

                matched = result.get("matched_skills", [])

                if matched:
                    st.write(
                        "**Matching skills:** "
                        + ", ".join(matched)
                    )
                else:
                    st.write(
                        "No listed skills matched yet. "
                        "You can build toward this role step by step."
                    )

            with right:
                st.metric(
                    "Skill match",
                    f"{result['match_score']}%",
                )

            st.progress(
                max(0, min(result["match_score"], 100)) / 100
            )

    # ----------------------------------------------
    # SKILL GAP ANALYSIS
    # ----------------------------------------------
    st.divider()

    st.markdown(
        f'<div class="section-heading">🪴 4. Your Skill Gap: {target_role}</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Every career journey starts somewhere. "
        "See which listed skills you have and which you can develop."
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Skill coverage",
            f"{gap['coverage_score']}%",
        )

    with metric2:
        st.metric(
            "Skills matched",
            len(gap["matched_skills"]),
        )

    with metric3:
        st.metric(
            "Skills to develop",
            len(gap["missing_skills"]),
        )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("💚 Skills You Have")

            if gap["matched_skills"]:
                for skill in gap["matched_skills"]:
                    st.write(f"✅ {skill.title()}")
            else:
                st.write("No listed skills matched yet.")

    with col2:
        with st.container(border=True):
            st.subheader("📚 Skills to Develop")

            if gap["missing_skills"]:
                for skill in gap["missing_skills"]:
                    st.write(f"🌱 {skill.title()}")
            else:
                st.success(
                    "You cover all the listed skills for this role!"
                )

    # ----------------------------------------------
    # PERSONALIZED LEARNING ROADMAP
    # ----------------------------------------------
    st.divider()

    st.markdown(
        '<div class="section-heading">🗺️ 5. Your Learning Roadmap</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Turn your skill gaps into small, practical steps. "
        "Choose one skill at a time and keep learning."
    )

    roadmap = generate_roadmap(gap["missing_skills"])

    if roadmap:

        for number, item in enumerate(roadmap, start=1):

            with st.container(border=True):

                st.subheader(
                    f"Step {number}: {item['skill'].title()}"
                )

                st.write("**📖 Learning activity**")
                st.write(item["activity"])

                st.write("**🛠️ Practice project**")
                st.write(item["project"])

                resource_url = item.get("resource")

                if resource_url:
                    st.link_button(
                        "🔗 Open Learning Resource",
                        resource_url,
                    )

    else:
        st.success(
            "You cover all the listed skills for this role! "
            "Try building a portfolio project to demonstrate your abilities."
        )

    # ----------------------------------------------
    # RESPONSIBLE AI INFORMATION
    # ----------------------------------------------
    st.divider()

    with st.expander("ℹ️ About these recommendations"):

        st.write(
            "This prototype uses sample job data, selected skills, "
            "and keyword-based resume detection. Resume detection can "
            "miss skills expressed in different words, and scanned PDFs "
            "may not be readable. Review detected skills carefully."
        )

        st.write(
            "Recommendations support career exploration. "
            "They do not guarantee employment or replace professional advice."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: #F0EEFF;
        border-radius: 16px;
        color: #403A60;
    ">
        <strong>🌈 InclusiveCareer AI</strong><br>
        Skills Over Barriers, Opportunities for Everyone.<br>
        <small>Learn at your own pace. Build your future your way.</small>
    </div>
    """,
    unsafe_allow_html=True,
)
