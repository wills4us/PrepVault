import streamlit as st
from auth import login, signup

def show_login():
    st.subheader("🔐 Login or Sign Up")

    tabs = st.tabs(["Login", "Sign Up"])

    # --- LOGIN TAB ---
    with tabs[0]:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            success, msg = login(username, password)
            if success:
                st.session_state.username = username
                st.success(f"✅ {msg} Welcome back, {username}!")
            else:
                st.error(f"❌ {msg}")

    # --- SIGNUP TAB ---
    with tabs[1]:
        new_user = st.text_input("Choose a username", key="signup_user")
        new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
        email = st.text_input("Email address (optional)", key="signup_email")

        if st.button("Sign Up"):
            if not new_user or not new_pass:
                st.warning("Username and password cannot be empty.")
            else:
                success, msg = signup(new_user, new_pass, email=email, role="user")
                if success:
                    st.success(f"🎉 {msg} You can now log in.")
                    st.session_state.username = new_user
                else:
                    st.warning(f"⚠️ {msg}")
