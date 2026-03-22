import streamlit as st
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
</style>
""", unsafe_allow_html=True)

import PyPDF2

from skills import skills_db
from jobs import jobs
from utils import *

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠")

st.title("🧠 AI Resume Analyzer")
st.write("Upload your resume and get smart career insights 🚀")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if uploaded_file:
    text = extract_text(uploaded_file)
    text = clean_text(text)

    st.success("✅ Resume analyzed successfully!")

    detected_skills = extract_skills(text, skills_db)

    st.subheader("✅ Detected Skills")
    for skill in detected_skills:
        st.write(f"✅ {skill}")

    job_scores = get_best_jobs(detected_skills, jobs)

    st.subheader("💼 Best Job Matches")

    col1, col2, col3 = st.columns(3)

    top_jobs = list(job_scores.items())[:3]

    cols = [col1, col2, col3]

    for i, (job, score) in enumerate(top_jobs):
        cols[i].metric(label=job, value=f"{score}%")

    top_job = list(job_scores.keys())[0]
    top_score = job_scores[top_job]

    st.subheader("📊 Resume Score")
    st.progress(top_score / 100)
    st.write(f"{top_score}% match for {top_job}")
    st.subheader("🧾 Final Analysis")

    if top_score >= 70:
        st.success("🎯 Your resume is strong for this role!")
    elif top_score >= 40:
        st.warning("⚡ Good profile, but needs improvement.")
    else:
        st.error("❗ Your resume needs significant improvement.")

        missing = get_missing_skills(detected_skills, jobs[top_job])

        st.subheader(f"📉 Skills Missing for {top_job}")
        
        st.subheader("💡 Suggestions to Improve")
        for skill in missing:
            st.write(f"❌ {skill}")

        
        if missing:
            for skill in missing[:5]:
                st.write(f"👉 Learn {skill} to improve your profile")
        else:
            st.success("🎉 Your resume is strong for this role!")
            st.subheader("🚀 Profile Strength")

        if "python" in detected_skills:
            st.write("✅ Strong Python foundation")

        if "git" in detected_skills:
            st.write("✅ Version control knowledge (Git)")

        if "data science" in detected_skills:
            st.write("✅ Exposure to Data Science concepts")    