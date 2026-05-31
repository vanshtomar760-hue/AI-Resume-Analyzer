import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background:linear-gradient(90deg,#00c6ff,#0072ff);
text-align:center;
margin-bottom:20px;
">
<h1 style="color:white;">
🤖 AI Resume Analyzer
</h1>
<p style="color:white;">
Analyze resumes, ATS score & skill gaps instantly
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stButton > button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(0,114,255,0.6);
}

</style>
""", unsafe_allow_html=True)

job_description = st.text_area(
    "Paste Job Description Here"
)

skills_list = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pandas",
    "numpy",
    "html",
    "css",
    "javascript"
]

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("Analyze Resume")

with col2:
    reset = st.button("Reset")


def extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_list:

        if skill in text:

            found_skills.append(skill)

    return found_skills


def calculate_score(resume, jd):

    cv = CountVectorizer()

    matrix = cv.fit_transform(
        [resume, jd]
    )

    similarity = cosine_similarity(
        matrix
    )[0][1]

    return round(
        similarity * 100,
        2
    )


def extract_resume_sections(text):

    data = {}

    lines = text.split("\n")

    data["Name"] = (
        lines[0]
        if len(lines) > 0
        else "No"
    )

    education_keywords = [
        "b.tech",
        "bachelor",
        "undergraduate",
        "college",
        "university"
    ]

    education = []

    for line in lines:

        if any(
            word in line.lower()
            for word in education_keywords
        ):

            education.append(line)

    data["Education"] = (
        education
        if education
        else ["No"]
    )


    exp_keywords = [
        "experience",
        "intern",
        "worked"
    ]

    experience = []

    for line in lines:

        if any(
            word in line.lower()
            for word in exp_keywords
        ):

            experience.append(line)

    data["Experience"] = (
        experience
        if experience
        else ["No"]
    )

    return data



if uploaded_file and analyze:

    resume_text = extract_text(
        uploaded_file
    )

    parsed = extract_resume_sections(
        resume_text
    )

    skills_found = extract_skills(
        resume_text
    )

    st.subheader("🛠 Skills Found")

    cols = st.columns(4)

    for i, skill in enumerate(skills_found):

        cols[i % 4].success(skill.title())

    st.metric(
    "Total Skills Found",
    len(skills_found)
)

    st.subheader(
        "Resume Details"
    )

    st.write("Name")

    st.success(
        parsed["Name"]
    )


    st.write("Education")

    for item in parsed["Education"]:

        st.info(item)

    if job_description:

        score = calculate_score(
            resume_text,
            job_description
        )

        st.subheader(
            "ATS Match Score"
        )

        if score < 30:

         st.error(
        f"🔴 ATS Score: {score}%"
    )

        elif score < 50:

         st.warning(
        f"🟡 ATS Score: {score}%"
    )

        else:

         st.success(
        f"🟢 ATS Score: {score}%"
    )
        st.progress(
            int(score)
        )


        jd_skills = extract_skills(
            job_description
        )

        missing_skills = []

        for skill in jd_skills:

            if skill not in skills_found:

                missing_skills.append(
                    skill
                )


                st.subheader("⚠ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"❌ {skill.title()}"
                )

        else:

            st.success(
                "No important skills missing"
            )

        st.subheader("📈 Skills Analysis")

        matched = len(skills_found) - len(missing_skills)

        labels = [
            "Matched",
            "Missing"
        ]

        sizes = [
            matched,
            len(missing_skills)
        ]

        fig, ax = plt.subplots()

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%"
        )

        ax.axis("equal")

        st.pyplot(fig)

        st.subheader("💡 Suggestions")

    if missing_skills:

        for skill in missing_skills:

         st.info(
            f"Consider adding {skill.title()} if you have worked with it."
        )

    if score < 50:

        st.warning(
        "Your resume has a low match with this job description."
    )

    elif score < 75:

        st.info(
        "Your resume partially matches the job requirements."
    )

    else:

        st.success(
        "Your resume strongly matches the job requirements."
    )


st.markdown("---")

st.markdown(
    """
    <div style="
    text-align:center;
    color:gray;
    ">
    Built by Vansh Tomar |
    Python • Streamlit • NLP
    </div>
    """,
    unsafe_allow_html=True
)
if reset:

    st.rerun()