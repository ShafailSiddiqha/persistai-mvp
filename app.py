import streamlit as st
import json, os

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="PersistAI – ADHD Flow MVP", page_icon="⚡", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FDFBFF 0%, #F7F9FF 100%);
    font-family: 'Poppins', sans-serif;
    color: #2C2C2C;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
    border-right: 1px solid #E2E8F0;
}
h1, h2, h3 {
    color: #5A3EBA;
    font-weight: 700;
}
.stButton>button {
    background: linear-gradient(90deg, #A1C4FD, #C2E9FB);
    color: #1E1E2E;
    border-radius: 10px;
    border: none;
    padding: 0.4rem 1rem;
    box-shadow: 0 3px 10px rgba(120,120,160,0.2);
    transition: 0.2s ease-in-out;
}
.stButton>button:hover { transform: scale(1.05); }
[data-testid="stMetricValue"] { color: #F87272 !important; }
[data-testid="stProgressBar"] div div {
    background: linear-gradient(90deg,#A1C4FD,#C2E9FB);
}
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg,#C2E9FB,#A1C4FD);
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA SESSION ----------
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "xp" not in st.session_state:
    st.session_state["xp"] = 0

# ---------- HEADER ----------
st.title("⚡ PersistAI – ADHD Flow MVP")
st.caption("Smart Parent–Child Agent System | ADHD Flow | XP Gamification")

# ---------- ABOUT SECTION ----------
with st.expander("💡 About this Project", expanded=True):
    st.markdown("""
    ### 🧠 Overview  
    **PersistAI** is a smart task-flow tracker for individuals with **ADHD or focus-related challenges**.  
    It helps you plan and complete tasks according to your **energy and attention levels**.

    ### 🎯 Purpose  
    Created for the **Persist Ventures AI Challenge**, this MVP demonstrates how adaptive task systems  
    can help manage productivity in a gentle, gamified, ADHD-friendly way.

    ### ⚙️ How to Use  
    - Adjust the **Energy Slider** below based on how you feel right now.  
    - Go to the **Tasks Manager** (sidebar) to **add, complete, or delete** tasks.  
    - Earn **XP** for completing tasks and check your weekly report anytime.  

    ### ❤️ Why it Matters  
    Instead of punishing inconsistency, this app **celebrates small wins**  
    and helps you align your focus cycles with achievable goals.
    """)

st.divider()

# ---------- ENERGY SECTION ----------
st.subheader("How energetic do you feel today?")
energy = st.slider("Energy Level", 0, 100, 60, help="Adjust based on how focused or motivated you feel right now.")

if energy < 40:
    st.warning("Low energy 💤 — Try light or creative tasks today.")
elif energy < 70:
    st.info("Moderate energy ⚙️ — Medium tasks are perfect today.")
else:
    st.success("High energy ⚡ — You’re ready for a challenge!")

st.divider()

# ---------- DASHBOARD ----------
st.header("🎮 Dashboard")
xp = st.session_state["xp"]
completed = len([t for t in st.session_state["tasks"] if t.get("completed")])
level = xp // 100 + 1

col1, col2, col3 = st.columns(3)
col1.metric("Level", level)
col2.metric("XP", xp)
col3.metric("Tasks Done", completed)

st.progress(min(1.0, xp / 500))
st.caption("🌱 Calm · Focused · Rewarding — Built for ADHD Flow")

st.markdown("<center><small>Built by <b>Shafail Siddiqha</b> for Persist Ventures AI Assignment</small></center>", unsafe_allow_html=True)
