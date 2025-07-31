import streamlit as st
import random
import os
import pandas as pd

# Predefined questions for each role
ROLE_QUESTIONS = {
    "Data Analyst": [
        "Can you explain the difference between inner join and outer join in SQL?",
        "How do you handle missing data when analyzing a dataset?",
        "Which tools do you use for data visualization and why?",
        "Describe a project where you uncovered an insight that changed a business decision.",
        "How do you ensure the accuracy of your analysis?"
    ],
    "Data Scientist": [
        "Explain the difference between supervised and unsupervised learning.",
        "What’s your approach to feature engineering?",
        "How do you evaluate the performance of a machine learning model?",
        "Describe a project where you used machine learning to solve a problem.",
        "What’s the difference between overfitting and underfitting?"
    ],
    "Python Developer": [
        "What are Python decorators and how are they used?",
        "Explain the difference between a list, tuple, and set.",
        "How do you handle exceptions in Python?",
        "Describe your experience with web frameworks like Flask or Django.",
        "What are Python generators and why are they useful?"
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

def generate_followup(role, user_response):
    if not user_response.strip():
        return "No response entered."
    return f"Follow-up: {random.choice(FOLLOWUP_TEMPLATES)}\nFeedback: {random.choice(FEEDBACK_TIPS)}"

def generate_mock_rating(user_response):
    length_score = min(len(user_response.strip()) // 50, 5)
    quality_score = random.randint(2, 5)  # Simulating feedback range
    avg_score = (length_score + quality_score) / 2
    return round(avg_score, 1)

def show_interview_simulator():
    st.subheader("🎤 AI Interview Simulator")
    st.markdown("Select a role to begin your simulated interview. AI will ask relevant questions for practice.")

    role = st.selectbox("💼 Select Interview Role", list(ROLE_QUESTIONS.keys()))

    if st.button("Start Interview"):
        st.markdown("---")
        st.markdown(f"### 🔹 Interview Questions for **{role}**")
        questions = ROLE_QUESTIONS.get(role, [])
        selected_questions = random.sample(questions, k=min(3, len(questions)))
        for idx, q in enumerate(selected_questions):
            st.write(f"**Q{idx+1}:** {q}")
            user_response = st.text_area(f"Your Answer to Q{idx+1}", key=f"response_{idx}")
            if user_response:
                feedback = generate_followup(role, user_response)
                rating = generate_mock_rating(user_response)
                st.markdown(f"✅ **AI Feedback:**\n{feedback}")
                st.markdown(f"⭐ **Mock Rating:** {rating} / 5")
