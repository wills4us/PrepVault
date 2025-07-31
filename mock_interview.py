# mock_interview.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime

QUESTION_BANK = {
    "Data Analyst": [
        "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
        "Explain the steps you take when cleaning a dataset.",
        "How would you handle missing values in a dataset?",
        "Describe a project where you used data visualization to drive decisions.",
        "What is the difference between correlation and causation?"
    ],
    "Frontend Developer": [
        "What is the Virtual DOM in React?",
        "How do you manage component state in React?",
        "Explain the difference between CSS Grid and Flexbox.",
        "What are web accessibility best practices?",
        "How do you optimize a website’s performance?"
    ]
}

def show_mock_interview(username):
    st.title("🧠 AI-Powered Mock Interview")

    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "response" not in st.session_state:
        st.session_state.response = ""

    st.markdown("This mock interview tool provides dynamic questions based on your selected role. Your responses will be rated and saved.")

    role = st.selectbox("Select your target role", list(QUESTION_BANK.keys()))
    st.session_state.role = role

    if st.button("➡️ Next Question"):
        st.session_state.current_question = random.choice(QUESTION_BANK[role])
        st.session_state.response = ""

    if st.session_state.current_question:
        st.markdown(f"### ❓ {st.session_state.current_question}")
        st.session_state.response = st.text_area("Your Answer", value=st.session_state.response, height=200)

        if st.button("✅ Submit Answer"):
            rating = random.randint(3, 5)  # Simulated rating for demo
            feedback = generate_feedback(st.session_state.response)

            save_response(
                username=username,
                role=st.session_state.role,
                question=st.session_state.current_question,
                response=st.session_state.response,
                rating=rating,
                feedback=feedback
            )

            st.success("Answer submitted and saved! ✅")
            st.markdown(f"⭐ **AI Rating:** {rating}/5")
            st.markdown(f"📝 **AI Feedback:** _{feedback}_")

def generate_feedback(response):
    length = len(response.split())
    if length < 20:
        return "Try elaborating more with examples or technical details."
    elif length < 50:
        return "Good effort. Include metrics, tools, or outcomes for a stronger answer."
    else:
        return "Well-structured response. Consider refining the flow and staying concise."

def save_response(username, role, question, response, rating, feedback):
    file_path = "data/interview_scores.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = {
        "Username": username,
        "Name": username,
        "Role": role,
        "Question": question,
        "Response": response,
        "Rating": rating,
        "Feedback": feedback,
        "Timestamp": timestamp
    }

    if not os.path.exists(file_path):
        df = pd.DataFrame([new_row])
    else:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(file_path, index=False)
