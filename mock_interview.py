# mock_interview.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime

ROLE_QUESTIONS = {
    "Data Analyst": [
        "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
        "Explain the steps you take when cleaning a dataset.",
        "How would you handle missing values in a dataset?",
        "Describe a project where you used data visualization to drive decisions.",
        "What is the difference between correlation and causation?"
        "How do you approach cleaning and preparing a large dataset for analysis?"
        "Can you describe a time you used data to solve a business problem or make a recommendation?"
        "How do you handle missing or inconsistent data in your analysis?"
        "What’s the most complex dashboard or report you’ve built, and how did it support decision-making?"
    ],
    "Data Scientist": [
        "Explain the difference between supervised and unsupervised learning.",
        "What’s your approach to feature engineering?",
        "How do you evaluate the performance of a machine learning model?",
        "Describe a project where you used machine learning to solve a problem.",
        "What’s the difference between overfitting and underfitting?"
        "How do you ensure your model is not overfitting?"
        "Tell me about a time when your analysis or model directly influenced a business decision."
        "Describe a project where you built a predictive model. What was the goal, and how did you evaluate its performance?"
        
    ],
    "Python Developer": [
        "What are Python decorators and how are they used?",
        "Explain the difference between a list, tuple, and set.",
        "How do you handle exceptions in Python?",
        "Describe your experience with web frameworks like Flask or Django.",
        "What are Python generators and why are they useful?"
        "What are Python’s key data types, and when would you use each one (list, tuple, set, dictionary)?"
        "Can you explain the difference between deep copy and shallow copy in Python?"
        "Describe a project where you used Python to automate a task or process."
        "How do you manage dependencies and environments in a Python project?"
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

# Offline rule-based follow-up system
FOLLOWUP_TEMPLATES = [
    "Can you provide an example to support your answer?",
    "How has this skill helped you in a past experience?",
    "What challenges did you face and how did you overcome them?",
    "What tools or methods did you use in that situation?",
    "Would you do anything differently if faced with that again?"
]

FEEDBACK_TIPS = [
    "Try to provide a concrete example to make your response stronger.",
    "Keep your answers concise but detailed.",
    "Structure your answer using the STAR method (Situation, Task, Action, Result).",
    "Highlight specific tools or metrics to support your response.",
    "Avoid generic responses—tailor them to the role you're applying for."
]


def show_mock_interview(username):
    st.subheader("🎤 AI Interview Simulator")
    st.markdown("Select a role to begin your simulated interview. You will be asked questions one by one.")

    role = st.selectbox("💼 Select Interview Role", list(ROLE_QUESTIONS.keys()), key="role_select")

    if "interview_state" not in st.session_state:
        st.session_state.interview_state = {
            "questions": [],
            "current_index": 0,
            "started": False,
            "response": ""
        }

    if st.button("Start Interview"):
        questions = random.sample(ROLE_QUESTIONS.get(role, []), k=min(3, len(ROLE_QUESTIONS[role])))
        st.session_state.interview_state.update({
            "questions": questions,
            "current_index": 0,
            "started": True,
            "response": ""
        })

    if st.session_state.interview_state["started"]:
        questions = st.session_state.interview_state["questions"]
        index = st.session_state.interview_state["current_index"]

        if index < len(questions):
            q = questions[index]
            st.markdown(f"**Question {index + 1} of {len(questions)}:** {q}")
            user_response = st.text_area("Your Answer", value=st.session_state.interview_state.get("response", ""), key=f"response_{index}")

            if st.button("Submit Answer"):
                if user_response.strip():
                    feedback = generate_followup(role, user_response)
                    rating = generate_mock_rating(user_response)

                    save_interview_score(username, role, q, user_response, feedback, rating)

                    st.success("✅ Response saved.")
                    st.markdown(f"🧠 **AI Feedback:** {feedback}")
                    st.markdown(f"⭐ **Mock Rating:** {rating} / 5")

                    st.session_state.interview_state["response"] = ""
                else:
                    st.warning("Please enter a response before submitting.")

            if st.button("Next Question"):
                st.session_state.interview_state["current_index"] += 1
                st.session_state.interview_state["response"] = ""
        else:
            st.success("🎉 Interview completed! All responses have been recorded.")

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
