import streamlit as st
import tempfile
import time
import re

from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity
from utils.skill_gap import find_skill_gap
from utils.resume_feedback import generate_feedback
from utils.logger import log_activity
from utils.login_logger import save_login


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("user", None)
st.session_state.setdefault("theme", "Light")
st.session_state.setdefault("history", [])
st.session_state.setdefault("session_start", time.time())

st.session_state.setdefault("profile", {
    "name": "",
    "role": "",
    "experience": ""
})

st.session_state.setdefault("notifications", {
    "email": False,
    "job_alerts": False,
    "resume_tips": False
})


# ---------------- THEME FUNCTION ----------------
def apply_theme():

    if st.session_state.theme == "Dark":

        st.markdown("""
        <style>

        .stApp {
            background-color:#0f172a;
            color:#e5e7eb;
        }

        section[data-testid="stSidebar"] {
            background-color:#111827;
        }

        h1,h2,h3,h4,h5,h6,p,label {
            color:#e5e7eb;
        }

        .stButton>button {
            background-color:#3b82f6;
            color:white;
            border-radius:8px;
        }

        .stMetric {
            background-color:#1f2937;
            padding:10px;
            border-radius:10px;
        }

        </style>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>

        .stApp {
            background-color:#f9fafb;
            color:#111827;
        }

        section[data-testid="stSidebar"] {
            background-color:#ffffff;
        }

        h1,h2,h3,h4,h5,h6,p,label {
            color:#111827;
        }

        .stButton>button {
            background-color:#2563eb;
            color:white;
            border-radius:8px;
        }

        .stMetric {
            background-color:#ffffff;
            padding:10px;
            border-radius:10px;
        }

        </style>
        """, unsafe_allow_html=True)


apply_theme()


# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 Resume AI")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Analyzer", "⚙️ Settings", "👤 Profile", "ℹ️ About"]
)


# ---------------- LOGIN ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Account")

if st.session_state.user:

    st.sidebar.success(f"Logged in as {st.session_state.user}")

    if st.sidebar.button("Logout"):
        log_activity(st.session_state.user, "logout", {})
        st.session_state.user = None
        st.rerun()

else:

    with st.sidebar.expander("🔐 Login with Gmail"):

        email = st.text_input("Enter Gmail")

        if st.button("Login"):

            if re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):

                st.session_state.user = email
                save_login(email)

                st.success("Login successful")
                st.rerun()

            else:
                st.error("Enter a valid Gmail address")


# ---------------- NOTIFICATION BELL ----------------
col1, col2 = st.columns([9,1])

with col2:

    if st.button("🔔"):

        if st.session_state.notifications["job_alerts"]:
            st.toast("New job matches available!")

        elif st.session_state.notifications["resume_tips"]:
            st.toast("New resume improvement tips!")

        else:
            st.toast("No new notifications")


# ======================================================
# SETTINGS PAGE
# ======================================================

if page == "⚙️ Settings":

    st.title("⚙️ Settings")

    tab1, tab2 = st.tabs(
        ["🎨 Appearance", "🔔 Notifications"]
    )

    # -------- Appearance --------
    with tab1:

        st.subheader("Theme Settings")

        theme_option = st.selectbox(
            "Theme Mode",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        if st.button("Apply Theme"):

            st.session_state.theme = theme_option
            st.success("Theme updated")
            st.rerun()

    # -------- Notifications --------
    with tab2:

        st.subheader("Notification Preferences")

        email_notifications = st.checkbox(
            "Email Notifications",
            value=st.session_state.notifications["email"]
        )

        resume_tips = st.checkbox(
            "Resume Tips",
            value=st.session_state.notifications["resume_tips"]
        )

        if st.button("Save Notification Settings"):

            st.session_state.notifications["email"] = email_notifications
            st.session_state.notifications["job_alerts"] = job_alerts
            st.session_state.notifications["resume_tips"] = resume_tips

            st.success("Notification settings saved")


# ======================================================
# PROFILE PAGE
# ======================================================

elif page == "👤 Profile":

    st.title("👤 Profile")

    if st.session_state.user:

        name = st.text_input(
            "Full Name",
            value=st.session_state.profile["name"]
        )

        role = st.selectbox(
            "Career Role",
            ["Student","Data Scientist","AI Engineer","Software Engineer"]
        )

        experience = st.selectbox(
            "Experience Level",
            ["Student","Junior","Mid-Level","Senior"]
        )

        avatar = st.file_uploader("Upload Profile Picture")

        if st.button("Update Profile"):

            st.session_state.profile["name"] = name
            st.session_state.profile["role"] = role
            st.session_state.profile["experience"] = experience

            st.success("Profile updated successfully")

    else:

        st.info("Login to edit profile")


# ======================================================
# ABOUT PAGE
# ======================================================

elif page == "ℹ️ About":

    st.title("About This App")

    st.write("""
AI Resume Analyzer helps users:

• Compare resumes with job descriptions  
• Detect missing skills  
• Improve career profiles  
• Get AI-powered feedback
""")


# ======================================================
# ANALYZER PAGE
# ======================================================

elif page == "🏠 Analyzer":

    st.markdown("""
    <h1 style='text-align:center;color:#2563eb'>
    AI Resume Analyzer
    </h1>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;color:gray'>Smart Resume Matching • Skill Gap Detection • Career Insights</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

    with col2:
        job_description = st.text_area("Paste Job Description")

    analyze_btn = st.button("Analyze Resume")

    if analyze_btn:

        if uploaded_file and job_description:

            with st.spinner("Analyzing resume..."):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    path = tmp.name

                resume_text = extract_text_from_pdf(path)

                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

                match_score = calculate_similarity(resume_text, job_description)

                missing_skills = find_skill_gap(resume_skills, job_skills)

                feedback = generate_feedback(match_score, missing_skills)

            st.metric("Match Score", f"{match_score}%")
            st.progress(match_score/100)

            st.subheader("Missing Skills")
            st.write(missing_skills)

            st.subheader("Feedback")

            for f in feedback:
                st.write("✔", f)

            st.session_state.history.append({
                "score": match_score,
                "missing": missing_skills
            })

        else:

            st.warning("Upload resume and paste job description.")


# ---------------- HISTORY ----------------
st.divider()
st.subheader("📜 Analysis History")

for item in st.session_state.history:

    st.write(
        "Score:", item["score"],
        "| Missing:", item["missing"]
    )


# ---------------- SESSION TRACKING ----------------
if st.session_state.user:

    session_duration = int(time.time() - st.session_state.session_start)

    log_activity(
        st.session_state.user,
        "session_time",
        {"seconds": session_duration}
    )