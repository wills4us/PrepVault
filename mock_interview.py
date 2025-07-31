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

def show_interview_simulator(username):
    st.subheader("🎤 AI Interview Simulator")
    st.markdown(f"Hello **{username.title()}**, let's begin your personalized mock interview.")
    
    role = st.selectbox("💼 Select Interview Role", list(ROLE_QUESTIONS.keys()))
    
    if 'asked_questions' not in st.session_state:
        st.session_state.asked_questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    if 'role_selected' not in st.session_state:
        st.session_state.role_selected = ""
    if 'completed_questions' not in st.session_state:
        st.session_state.completed_questions = 0

    if role != st.session_state.role_selected:
        # Reset if role changes
        st.session_state.asked_questions = []
        st.session_state.current_question = ""
        st.session_state.role_selected = role
        st.session_state.completed_questions = 0

    questions = ROLE_QUESTIONS.get(role, [])

    # If 3 questions already done
    if st.session_state.completed_questions >= 3:
        st.success("✅ You've completed the mock interview.")
        return

    # Load question if empty
    if st.session_state.current_question == "":
        remaining = list(set(questions) - set(st.session_state.asked_questions))
        if remaining:
            st.session_state.current_question = random.choice(remaining)
            st.session_state.asked_questions.append(st.session_state.current_question)

    question = st.session_state.current_question
    st.markdown(f"**Q{st.session_state.completed_questions + 1}: {question}**")

    user_response = st.text_area("Your Answer", key=f"response_{st.session_state.completed_questions}")

    if st.button("✅ Submit Answer"):
        if not user_response.strip():
            st.warning("Please provide a response.")
        else:
            feedback = generate_followup(role, user_response)
            rating = generate_mock_rating(user_response)

            # Save to CSV
            save_interview_score(username, role, question, user_response, feedback, rating)

            st.markdown(f"🧠 **AI Feedback:**\n{feedback}")
            st.markdown(f"⭐ **Mock Rating:** `{rating} / 5`")

            if st.button("➡️ Next Question"):
                st.session_state.current_question = ""
                st.session_state.completed_questions += 1

def save_interview_score(username, role, question, response, feedback, score):
    file = "data/interview_scores.csv"
    os.makedirs("data", exist_ok=True)
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=["Name", "Role", "Question", "Response", "Feedback", "Rating"])

    new_row = {
        "Name": username,
        "Role": role,
        "Question": question,
        "Response": response,
        "Feedback": feedback,
        "Rating": score
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(file, index=False)
