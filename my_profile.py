import streamlit as st
import pandas as pd
import os

# --- Constants ---
RESUME_SUMMARY_FILE = "resumes/resume_scores.csv"
PROFILE_IMG_DIR = "profile_images"
USER_INFO_FILE = "user_info.csv"

# --- Ensure directories and files exist ---
os.makedirs(PROFILE_IMG_DIR, exist_ok=True)
if not os.path.exists(USER_INFO_FILE):
    pd.DataFrame(columns=["username", "email", "location", "bio"]).to_csv(USER_INFO_FILE, index=False)


# --- Utility Functions ---
def load_user_resume_summary(username):
    if os.path.exists(RESUME_SUMMARY_FILE):
        df = pd.read_csv(RESUME_SUMMARY_FILE)
        return df[df["username"] == username]
    return pd.DataFrame()


def generate_study_plan(missing_keywords):
    plan = []
    for keyword in missing_keywords:
        kw = keyword.lower()
        if "excel" in kw:
            plan.append("📊 Take a Microsoft Excel course (pivot tables, formulas, charts).")
        elif "sql" in kw:
            plan.append("🧮 Practice SQL queries on platforms like LeetCode or SQLBolt.")
        elif "python" in kw:
            plan.append("🐍 Complete a beginner-to-intermediate Python course.")
        elif "communication" in kw:
            plan.append("🗣️ Join a public speaking or communication skills workshop.")
        elif "power bi" in kw:
            plan.append("📈 Build dashboards in Power BI using sample datasets.")
        elif "data analysis" in kw:
            plan.append("📘 Enroll in a course on data wrangling, EDA, and visualization.")
        else:
            plan.append(f"📌 Research and build competence in **{keyword}**.")
    return plan


def get_profile_image(username):
    filepath = os.path.join(PROFILE_IMG_DIR, f"{username}.png")
    return filepath if os.path.exists(filepath) else None


def get_user_summary(username):
    if not os.path.exists(USER_INFO_FILE):
        return ""
    df = pd.read_csv(USER_INFO_FILE)
    user = df[df["username"] == username]
    return user.iloc[0].get("bio", "") if not user.empty else ""


# --- Profile View ---
def show_profile(username):
    st.markdown("### ✏️ Edit Profile")
    df = pd.read_csv(USER_INFO_FILE)
    user_row = df[df["username"] == username]

    if not user_row.empty:
        user_info = user_row.iloc[0]
        email = st.text_input("Email", user_info.get("email", ""))
        location = st.text_input("Location", user_info.get("location", ""))
        bio = st.text_area("Short Bio", user_info.get("bio", ""))
    else:
        email = st.text_input("Email")
        location = st.text_input("Location")
        bio = st.text_area("Short Bio")

    if st.button("💾 Save Profile"):
        updated = pd.DataFrame([{"username": username, "email": email, "location": location, "bio": bio}])
        df = df[df["username"] != username]
        df = pd.concat([df, updated], ignore_index=True)
        df.to_csv(USER_INFO_FILE, index=False)
        st.success("✅ Profile updated successfully!")

    # --- Profile Image ---
    st.markdown("### 🖼️ Profile Image")
    uploaded = st.file_uploader("Upload Profile Image", type=["png", "jpg", "jpeg"])
    if uploaded:
        img_path = os.path.join(PROFILE_IMG_DIR, f"{username}.png")
        with open(img_path, "wb") as f:
            f.write(uploaded.read())
        st.success("✅ Profile picture updated!")

    current_img = get_profile_image(username)
    if current_img:
        st.image(current_img, width=120, caption="Your current image")


# --- Study Plan Based on Resume Gaps ---
def show_study_plan(username):
    st.title("📘 Study Plan Builder")
    st.markdown("Tailored based on missing skills from your resume analysis.")

    summary = load_user_resume_summary(username)
    if summary.empty:
        st.info("No resume analysis found. Please upload and analyze a resume first.")
        return

    latest = summary.iloc[-1]

    if "missing_keywords" in latest and pd.notna(latest["missing_keywords"]):
        try:
            missing = eval(latest["missing_keywords"]) if isinstance(latest["missing_keywords"], str) else []
        except:
            missing = []

        if missing:
            st.markdown("### 🔍 Missing Skills:")
            st.write(", ".join(missing))

            st.markdown("### 📚 Suggested Study Plan:")
            plan = generate_study_plan(missing)
            for item in plan:
                st.write(item)

            if st.button("📥 Download Plan"):
                plan_text = "\n".join(plan)
                st.download_button(
                    label="Download as .txt",
                    data=plan_text,
                    file_name=f"{username}_study_plan.txt",
                    mime="text/plain"
                )
        else:
            st.success("🎉 No major skill gaps detected. You're well-prepared!")
    else:
        st.info("Missing keyword data not found in your resume analysis.")
