import streamlit as st
import os

# Import screens/modules
from dashboard import show_dashboard
from login_screen import show_login
from resume_analyzer import show_resume_review
from my_profile import show_profile

# --- App Config ---
st.set_page_config(page_title="PrepVault", layout="centered")
st.title("🎓 PrepVault - Career Readiness Suite")

# --- Welcome Tooltip ---
if "show_tip" not in st.session_state:
    st.session_state.show_tip = True

if st.session_state.show_tip:
    with st.expander("👋 Welcome to PrepVault!", expanded=True):
        st.markdown("""
        PrepVault is your career prep buddy!  
        • Analyze your resume 💼  
        • Practice interviews 🗣️  
        • Track your progress 📊  
        • Get AI guidance to boost your career 🚀
        """)
        if st.button("Got it!"):
            st.session_state.show_tip = False

# --- Navigation ---
menu = st.sidebar.radio("Navigate", ["Login", "Dashboard", "Resume Analyzer", "Mock Interview", "My Profile"],
                        help="Use this menu to explore PrepVault features.")

if "username" not in st.session_state:
    st.session_state.username = ""

# --- Logout Button ---
if st.session_state.username:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = ""
        st.success("You have been logged out.")
        st.experimental_rerun()

# --- Routing ---
if menu == "Login":
    show_login()

elif menu == "Dashboard":
    if st.session_state.username:
        show_dashboard(st.session_state.username)
    else:
        st.warning("Please log in to view your dashboard.")

elif menu == "Resume Analyzer":
    if st.session_state.username:
        show_resume_review(st.session_state.username)
    else:
        st.warning("Please log in to analyze your resume.")

elif menu == "Mock Interview":
    if st.session_state.username:
        from mock_interview import show_interview_simulator
        show_interview_simulator()
    else:
        st.warning("Please log in to access mock interviews.")

elif menu == "My Profile":
    if st.session_state.username:
        show_profile(st.session_state.username)
    else:
        st.warning("Please log in to access your profile.")
