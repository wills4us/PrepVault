import streamlit as st
import os
import pandas as pd
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Load transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Constants ---
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Job role descriptions
JOB_DESCRIPTIONS = {
    "Data Analyst": "Responsible for analyzing data, building dashboards, writing SQL queries, and delivering insights using tools like Python, Power BI, and Excel.",
    "Customer Support": "Handles customer issues via email or phone, uses CRM tools, ensures customer satisfaction, and communicates empathetically.",
    "HR": "Involved in recruitment, employee onboarding, payroll, enforcing HR policies, and managing employee relations.",
    "Python Developer": "Develops backend systems using Python, builds APIs, works with Flask or Django, and writes clean, efficient code.",
    "Power BI Analyst": "Creates dashboards and reports using Power BI, performs data modeling, DAX calculations, and collaborates with business teams.",
    "Admin": "Supports office tasks such as scheduling, data entry, communication, and administrative coordination."
}

# Expected keywords
ROLE_KEYWORDS = {
    "Data Analyst": ["sql", "excel", "python", "power bi", "data visualization", "statistics", "dashboard", "data cleaning"],
    "Customer Support": ["crm", "customer service", "ticketing", "communication", "email", "phone support", "problem resolution"],
    "HR": ["recruitment", "onboarding", "payroll", "employee relations", "compliance", "hr policies"],
    "Python Developer": ["python", "flask", "django", "rest api", "oop", "unit testing", "git", "debugging"],
    "Power BI Analyst": ["power bi", "dax", "data modeling", "dashboard", "kpi", "visualization", "m query"],
    "Admin": ["scheduling", "data entry", "ms office", "reporting", "documentation", "clerical"]
}

def extract_text_from_pdf(uploaded_file):
    """Extracts text or performs OCR if needed."""
    try:
        reader = PdfReader(uploaded_file)
        raw_text = " ".join([page.extract_text() or "" for page in reader.pages])
        if raw_text.strip():
            return raw_text.strip().lower()
    except Exception:
        pass

    # OCR fallback
    try:
        st.info("🔍 Trying OCR for image-based resume...")
        images = convert_from_path(uploaded_file.name, dpi=300)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        return ocr_text.strip().lower()
    except Exception as e:
        st.error(f"❌ OCR Failed: {e}")
        return ""

def identify_missing_keywords(resume_text, job_role):
    required = ROLE_KEYWORDS.get(job_role, [])
    return [kw for kw in required if kw not in resume_text.lower()]

def ai_match_resume_to_roles(resume_text):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    scores = {}
    for role, desc in JOB_DESCRIPTIONS.items():
        desc_embedding = model.encode(desc, convert_to_tensor=True)
        similarity = util.cos_sim(resume_embedding, desc_embedding).item()
        scores[role] = round(similarity * 100, 2)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def display_past_attempts(username):
    df_path = os.path.join(UPLOAD_FOLDER, "resume_scores.csv")
    if os.path.exists(df_path):
        df = pd.read_csv(df_path)
        user_df = df[df["username"] == username]
        if not user_df.empty:
            st.markdown("### 📂 Past Attempts")
            st.dataframe(user_df.sort_values(by="match_score", ascending=False), use_container_width=True)

def analyze_resume(username, job_role):
    uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, f"{username}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Resume uploaded successfully!")

        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text:
            st.error("❌ No readable text found. Try uploading a text-based PDF or use OCR-compatible scans.")
            return

        st.markdown("### 🔎 Extracted Resume Preview")
        st.code(resume_text[:1000])

        # Compute match score
        role_desc = JOB_DESCRIPTIONS.get(job_role, "")
        selected_score = util.cos_sim(
            model.encode(resume_text, convert_to_tensor=True),
            model.encode(role_desc, convert_to_tensor=True)
        ).item() * 100

        ranked_roles = ai_match_resume_to_roles(resume_text)
        best_match, best_score = ranked_roles[0]

        st.markdown("### 🧠 AI Evaluation")
        st.write(f"**Target Role:** {job_role}")
        st.write(f"**Match Score:** `{round(selected_score, 2)}%`")
        if selected_score >= 80:
            st.success("🎯 Excellent match! Your resume aligns very well with this role.")
        elif selected_score >= 50:
            st.info("📝 Decent match. Improve by emphasizing relevant skills.")
        else:
            st.warning("⚠️ Weak match. Consider revising your resume.")

        if best_match != job_role:
            st.markdown("### 💡 Better Match Suggestion")
            st.info(f"🔁 You may be a better fit for **{best_match}** (**{best_score}% match**)")

        st.markdown("#### 🧭 Top 3 Role Matches:")
        for role, score in ranked_roles[:3]:
            st.write(f"- **{role}**: {score}%")

        missing = identify_missing_keywords(resume_text, job_role)
        if missing:
            st.markdown("### 🧩 Missing Keywords")
            for kw in missing:
                st.write(f"- ❌ {kw}")
        else:
            st.success("✅ All essential keywords are present.")

        # Save result
        result = {
            "username": username,
            "file": uploaded_file.name,
            "role": job_role,
            "match_score": round(selected_score, 2),
            "suggested_role": best_match,
            "suggested_score": round(best_score, 2),
        }

        df_path = os.path.join(UPLOAD_FOLDER, "resume_scores.csv")
        if os.path.exists(df_path):
            old = pd.read_csv(df_path)
            df = pd.concat([old, pd.DataFrame([result])], ignore_index=True)
        else:
            df = pd.DataFrame([result])
        df.to_csv(df_path, index=False)

        # Show previous history
        display_past_attempts(username)

def show_resume_review(username):
    st.subheader("📊 AI Resume Analyzer")
    st.markdown("Upload your resume and let AI assess your fit for your target job role.")
    job_role = st.selectbox("🎯 Select Target Role", list(JOB_DESCRIPTIONS.keys()))
    analyze_resume(username, job_role)
