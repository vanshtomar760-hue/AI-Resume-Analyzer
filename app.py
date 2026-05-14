import streamlit as st
import pdfplumber

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.title("AI Resume Analyzer")

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

analyze = st.button("Analyze Resume")
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

    st.subheader(
        "Skills Found"
    )

    st.success(
        skills_found
    )

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


    st.write("Work Experience")

    for item in parsed["Experience"]:

        st.info(item)


    if job_description:

        score = calculate_score(
            resume_text,
            job_description
        )

        st.subheader(
            "ATS Match Score"
        )

        st.metric(
            "Score",
            f"{score}%"
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


        st.subheader(
            "Missing Skills"
        )

        if missing_skills:

            st.error(
                missing_skills
            )

        else:

            st.success(
                "No important skills missing"
            )


        st.subheader(
            "Suggestions"
        )

        if score < 50:

            st.warning(
                "Add more relevant skills and projects."
            )

        elif score < 75:

            st.info(
                "Resume moderately matches the job."
            )

        else:

            st.success(
                "Strong resume match!"
            )


if reset:

    st.rerun()