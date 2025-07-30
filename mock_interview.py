import streamlit as st
import random
import os
import pandas as pd

# -------------------- Question Bank --------------------
INTERVIEW_QUESTIONS = {
    "Python": [
        "What are Python decorators and how are they used?",
        "Explain the difference between a list and a tuple.",
        "How does Python handle memory management?",
        "What are generators and why are they useful?",
        "How would you handle exceptions in Python?"
    ],
    "Power BI": [
        "What is DAX and how is it used in Power BI?",
        "How do you handle large datasets in Power BI?",
        "Explain the difference between a calculated column and a measure.",
        "How do you implement row-level security in Power BI?",
        "Describe your experience with Power BI dashboards."
    ],
    "Tableau": [
        "What are Tableau Extracts and how are they different from live connections?",
        "Explain the difference between discrete and continuous fields.",
        "How do you optimize the performance of a Tableau dashboard?",
        "What is a context filter?",
        "How do you handle user-level security in Tableau?"
    ],
    "SQL": [
        "What is normalization and why is it important?",
        "How would you write a query to find duplicate records in a table?",
        "What is the difference between WHERE and HAVING clauses?",
        "Explain different types of JOINs with examples.",
        "How do you optimize a slow-running query?"
    ],
    "Customer Support": [
        "How do you handle a difficult or angry customer?",
        "Describe a time you went above and beyond for a customer.",
        "What tools or platforms have you used in customer service?",
        "How do you prioritize multiple support tickets?",
        "How do you measure customer satisfaction?"
    ],
    "Admin": [
        "How do you manage scheduling and calendar conflicts?",
        "What office tools are you most comfortable with?",
        "Describe your experience organizing files or records.",
        "How do you handle confidential information?",
        "Give an example of how you managed multiple tasks efficiently."
    ],
    "HR": [
        "How do you ensure a fair recruitment process?",
        "What’s your experience with handling employee grievances?",
        "How do you manage conflict in the workplace?",
        "What key HR metrics do you track?",
        "Explain how you conduct performance reviews."
    ],
    "Customer Assistant": [
        "What would you do if a customer complains about a faulty product?",
        "How do you ensure customers feel valued?",
        "Tell me about a time you turned a negative situation into a positive one.",
        "How do you manage long queues or wait times?",
        "How do you stay calm under pressure?"
    ]
}

# -------------------- Paths --------------------
MOCK_LOG_FILE = "data/mock_logs.csv"
os.makedirs("data", exist_ok=True)

# -------------------- AI Feedback --------------------
def generate_mock_feedback(answer):
    if len(answer.split()) < 10:
        return "🧐 Your answer is too short. Try expanding with real examples and clarity.", 60
    elif "I" in answer and "because" in answer:
        return "✅ Strong response! Including reasons and personal actions strengthens your answer.", 85
    elif "not sure" in answer.lower():
        return "🤔 Be more confident. Even if unsure, show logical reasoning.", 50
    else:
        return "🎯 Good answer! You can improve by structuring your thoughts more clearly.", 75

# -------------------- Load History --------------------
def load_mock_logs():
    if os.path.exists(MOCK_LOG_FILE):
        return pd.read_csv(MOCK_LOG_FILE)
    return pd.DataFrame(columns=["Username", "Role", "Question", "Answer", "Score", "Feedback"])

def save_mock_response(username, role, question, answer, score, feedback):
    logs = load_mock_logs()
    new_entry = pd.DataFrame([{
        "Username": username,
        "Role": role,
        "Question": question,
        "Answer": answer,
        "Score": score,
        "Feedback": feedback
    }])
    updated_logs = pd.concat([logs, new_entry], ignore_index=True)
    updated_logs.to_csv(MOCK_LOG_FILE, index=False)

# -------------------- Show History --------------------
def show_mock_summary(username):
    logs = load_mock_logs()
    user_logs = logs[logs["Username"] == username]

    if not user_logs.empty:
        st.markdown("### 📊 Interview Performance Summary")
        st.dataframe(user_logs[["Role", "Question", "Score", "Feedback"]].sort_values(by="Score", ascending=False), use_container_width=True)

        avg_score = user_logs["Score"].mean()
        st.markdown(f"**📈 Average Score:** `{avg_score:.2f}`")

        st.markdown("#### 💡 AI Suggested Improvements")
        if avg_score < 70:
            st.warning("Try to elaborate more with examples. Focus on clarity and technical terms.")
        elif avg_score < 80:
            st.info("You're doing okay! Focus on structure and conciseness.")
        else:
            st.success("Great job! Keep refining with specific use-cases and results.")

# -------------------- Main UI --------------------
def show_mock_interview(username):
    st.subheader("🗣️ Mock Interview Practice")
    st.markdown(f"Welcome, **{username}**! Select a role and test your response to real-world questions.")

    role = st.selectbox("📌 Select Role", list(INTERVIEW_QUESTIONS.keys()))

    if st.button("🎯 Generate Question"):
        question = random.choice(INTERVIEW_QUESTIONS[role])
        st.session_state.mock_question = question
        st.session_state.mock_role = role
        st.session_state.mock_active = True

    if st.session_state.get("mock_active"):
        st.markdown("### ❓ Interview Question")
        st.info(st.session_state.mock_question)

        user_answer = st.text_area("✍️ Your Answer", height=200)

        if st.button("📝 Get Feedback"):
            if user_answer.strip():
                feedback, score = generate_mock_feedback(user_answer)
                st.markdown("### 📊 Feedback Summary")
                st.success(feedback)
                st.markdown(f"**🔢 Score:** `{score}`")

                save_mock_response(
                    username=username,
                    role=st.session_state.mock_role,
                    question=st.session_state.mock_question,
                    answer=user_answer,
                    score=score,
                    feedback=feedback
                )
                st.balloons()
            else:
                st.warning("Please enter your answer before requesting feedback.")

    # Show past summary
    show_mock_summary(username)
