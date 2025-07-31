import streamlit as st
import pandas as pd
import os
import plotly.express as px

DATA_DIR = "data"
RESUME_FILE = os.path.join(DATA_DIR, "resume_scores.csv")
INTERVIEW_FILE = os.path.join(DATA_DIR, "interview_scores.csv")

def show_profile_overview(username):
    st.subheader("👤 Profile Overview")

    resume_score = get_latest_resume_score(username)
    interview_score = get_average_interview_rating(username)

    st.markdown(f"**Name:** {username}")
    st.markdown(f"📄 **Latest Resume Score:** {resume_score} / 100")
    st.markdown(f"🎤 **Average Mock Interview Rating:** {interview_score} / 5")

def show_progress_summary(username):
    st.subheader("📊 Progress Summary")

    resume_df = load_user_resume_scores(username)
    interview_df = load_user_interview_scores(username)

    if not resume_df.empty:
        st.markdown("### Resume Scores Over Time")
        fig = px.line(resume_df, x="Date", y="Score", title="Resume Score Trend")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No resume scores found.")

    if not interview_df.empty:
        st.markdown("### Mock Interview Ratings")
        fig = px.bar(interview_df, x="Question", y="Rating", color="Role",
                     title="Interview Ratings", labels={"Rating": "Rating (out of 5)"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No interview responses found.")

# --- Helpers ---

def generate_mock_rating(response):
    # Example implementation
    if not response:
        return 0
    return len(response.split()) / 10  # Dummy logic

def get_latest_resume_score(username):
    if not os.path.exists(RESUME_FILE):
        return "N/A"
    df = pd.read_csv(RESUME_FILE)
    user_scores = df[df["Name"] == username]
    if user_scores.empty:
        return "N/A"
    return user_scores.sort_values("Date", ascending=False)["Score"].iloc[0]

def get_average_interview_rating(username):
    if not os.path.exists(INTERVIEW_FILE):
        return "N/A"
    df = pd.read_csv(INTERVIEW_FILE)
    user_scores = df[df["Name"] == username]
    if user_scores.empty:
        return "N/A"
    return round(user_scores["Rating"].mean(), 1)

def load_user_resume_scores(username):
    if not os.path.exists(RESUME_FILE):
        return pd.DataFrame()
    df = pd.read_csv(RESUME_FILE)
    user_scores = df[df["Name"] == username]
    return user_scores.sort_values("Date")

def load_user_interview_scores(username):
    if not os.path.exists(INTERVIEW_FILE):
        return pd.DataFrame()
    df = pd.read_csv(INTERVIEW_FILE)
    return df[df["Name"] == username]
