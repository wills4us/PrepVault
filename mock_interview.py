import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os

ROLE_QUESTIONS = {
    "Data Analyst": [
        "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
        "Explain the steps you take when cleaning a dataset.",
        "How would you handle missing values in a dataset?",
        "Describe a project where you used data visualization to drive decisions.",
        "What is the difference between correlation and causation?",
        "Can you describe a time you used data to solve a business problem or make a recommendation?",
        "What’s the most complex dashboard or report you’ve built, and how did it support decision-making?"
    ],
    "Data Scientist": [
        "Explain the difference between supervised and unsupervised learning.",
        "What’s your approach to feature engineering?",
        "How do you evaluate the performance of a machine learning model?",
        "Describe a project where you used machine learning to solve a problem.",
        "What’s the difference between overfitting and underfitting?",
        "Tell me about a time when your analysis influenced a business decision."
    ],
    "Python Developer": [
        "What are Python decorators and how are they used?",
        "Explain the difference between a list, tuple, and set.",
        "How do you handle exceptions in Python?",
        "Describe your experience with web frameworks like Flask or Django.",
        "What are Python generators and why are they useful?",
        "Describe a project where you used Python to automate a task or process."
    ],
    "Customer Care Assistant": [
        "How do you handle a difficult customer?",
        "What strategies do you use to remain calm under pressure?",
        "Describe a time you went above and beyond to assist a customer.",
        "How do you handle repetitive tasks and remain motivated?",
        "What would you do if you didn’t know how to answer a customer's question?"
    ],
    "Administrative Assistant": [
        "How do you prioritize tasks when managing multiple deadlines?",
        "Describe your experience with calendar management and scheduling.",
        "How do you handle confidential information?",
        "Describe a time you improved an administrative process.",
        "What tools or software are you most comfortable using for admin work?"
    ],
    "HR": [
        "How do you handle conflicts between employees?",
        "Describe your experience with recruitment and onboarding.",
        "What steps do you take to ensure HR policies are followed?",
        "How do you maintain confidentiality in sensitive HR matters?",
        "What’s your approach to employee engagement and retention?"
    ]
}

FOLLOWUP_TEMPLATES = [
    "Can you provide an example to support your answer?",
    "How has this skill helped you in a past experience?",
    "What challenges did you face and how did you overcome them?",
    "What tools or methods did you use in that situation?",
    "Would you do anything differently if faced with that again?"
]

def show_mock_interview(username):
    st.subheader("🎤 AI Interview Simulator")
    st.markdown("Select a role to begin your simulated interview.")
    role = st.selectbox("💼 Select Interview Role", list(ROLE_QUESTIONS.keys()), key="role_select")

    # --- Initialize session state ---
    if "interview" not in st.session_state:
        st.session_state.interview = {
            "started": False,
            "questions": [],
            "current": 0,
            "responses": [],
            "submitted": False,
            "last_response": ""
        }

    # --- Start interview ---
    if st.button("🚀 Start Interview"):
        st.session_state.interview = {
            "started": True,
            "questions": random.sample(ROLE_QUESTIONS[role], k=min(3, len(ROLE_QUESTIONS[role]))),
            "current": 0,
            "responses": [],
            "submitted": False,
            "last_response": ""
        }

    interview = st.session_state.interview

    if interview["started"]:
        current_idx = interview["current"]
        questions = interview["questions"]

        if current_idx < len(questions):
            current_question = questions[current_idx]
            st.markdown(f"**🧠 Question {current_idx + 1} of {len(questions)}:** {current_question}")

            response_key = f"response_{current_idx}"
            response = st.text_area("📝 Your Answer", key=response_key, value=interview["last_response"])

            if not interview["submitted"]:
                if st.button("✅ Submit Answer"):
                    if response.strip():
                        feedback = generate_followup(role, response)
                        rating = generate_mock_rating(response)
                        ideal_hint = generate_sample_ideal_answer(current_question)

                        save_interview_score(username, role, current_question, response, feedback, rating)

                        st.success("✅ Response saved.")
                        st.markdown(f"💬 **AI Feedback:** {feedback}")
                        st.markdown(f"⭐ **Mock Rating:** {rating} / 5")
                        st.markdown(f"💡 **Suggested Ideal Answer:** {ideal_hint}")

                        interview["responses"].append(response)
                        interview["submitted"] = True
                        interview["last_response"] = response
                    else:
                        st.warning("Please provide a response before submitting.")
            else:
                if st.button("➡️ Next Question"):
                    interview["current"] += 1
                    interview["submitted"] = False
                    interview["last_response"] = ""
        else:
            st.success("🎉 Interview Completed! All responses have been recorded.")

def generate_mock_rating(response):
    wc = len(response.strip().split())
    if wc < 10:
        return 2
    elif wc < 25:
        return 3
    elif wc < 50:
        return 4
    else:
        return 5

def generate_followup(role, response):
    if not response.strip():
        return "You didn't provide a response. Please try to give an example next time."
    if len(response.split()) < 20:
        return random.choice(FOLLOWUP_TEMPLATES)
    elif "team" in response.lower():
        return "Good mention of teamwork. Consider backing it with a scenario or outcome."
    elif "challenge" in response.lower():
        return "Nice point on challenges. Try using the STAR method to structure your response."
    else:
        return "Good response. You can improve it by being more specific or structured."

def generate_sample_ideal_answer(question):
    return "This question tests your understanding of core concepts. Use a specific example from your past to support your answer."

def save_interview_score(username, role, question, response, feedback, rating):
    file_path = "data/interview_scores.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = {
        "Username": username,
        "Role": role,
        "Question": question,
        "Response": response,
        "Feedback": feedback,
        "Rating": rating,
        "Timestamp": timestamp
    }

    if not os.path.exists(file_path):
        df = pd.DataFrame([new_row])
    else:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(file_path, index=False)
