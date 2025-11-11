import streamlit as st
import json, os, random, matplotlib.pyplot as plt

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="PersistAI – ADHD Flow MVP", page_icon="⚡", layout="centered")

# ---------- STYLES ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAF8FF 0%, #FDFBFF 100%);
    font-family: 'Poppins', sans-serif;
    color: #2C2C2C;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
    border-right: 1px solid #E2E8F0;
}
h1, h2, h3 { color: #5A3EBA; font-weight: 700; }
.stButton>button {
    background: linear-gradient(90deg, #A1C4FD, #C2E9FB);
    color: #1E1E2E;
    border-radius: 10px;
    border: none;
    box-shadow: 0 3px 10px rgba(120,120,160,0.2);
    transition: 0.2s ease-in-out;
}
.stButton>button:hover { transform: scale(1.05); }
[data-testid="stProgressBar"] div div {
    background: linear-gradient(90deg,#A1C4FD,#C2E9FB);
}
hr { border: none; height: 2px; background: linear-gradient(90deg,#C2E9FB,#A1C4FD); }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "tasks" not in st.session_state: st.session_state["tasks"] = []
if "xp" not in st.session_state: st.session_state["xp"] = 0
if "username" not in st.session_state: st.session_state["username"] = ""

# ---------- HEADER ----------
st.title("⚡ PersistAI – ADHD Flow MVP")
st.caption("Smart Parent–Child Agent System | ADHD Flow | XP Gamification")

# ---------- PERSONAL GREETING ----------
user_name = st.text_input("👋 What should I call you?", st.session_state["username"])
if user_name:
    st.session_state["username"] = user_name
    st.success(f"Hey {user_name}! Let’s make today productive 💪")

# ---------- MOTIVATIONAL QUOTES ----------
quotes = [
    "Small steps every day lead to big change 💫",
    "Don’t fight your rhythm — flow with it 🌊",
    "You’re doing better than you think 💛",
    "Progress > Perfection 🌻",
    "Energy flows where attention goes ⚡"
]
st.markdown(f"> 💬 **{random.choice(quotes)}**")

# ---------- ABOUT ----------
with st.expander("💡 About PersistAI"):
    st.markdown("""
    ### 🧠 Overview
    PersistAI helps ADHD minds stay in flow by aligning tasks with daily energy levels.
    It rewards consistency, not perfection, through XP-based gamification.
    
    ### 🎯 Features
    - Energy-aware task planning
    - XP leveling system 🎮
    - Weekly performance analytics 📊
    - Gentle motivational flow 💛
    
    ### 💻 Built For
    Persist Ventures AI Engineer Assignment (MVP Stage)
    """)

st.divider()

# ---------- ENERGY ----------
st.subheader("How energetic do you feel today?")
energy = st.slider("Energy Level", 0, 100, 60)

# AI-like task suggestions
if energy < 40:
    st.warning("🪫 Low energy — Do light or creative tasks like journaling or organizing.")
elif energy < 70:
    st.info("⚙️ Medium energy — Tackle analytical or medium-focus tasks.")
else:
    st.success("⚡ High energy — Time to crush a big project or hard task!")

st.divider()

# ---------- DASHBOARD ----------
xp = st.session_state["xp"]
completed = len([t for t in st.session_state["tasks"] if t.get("completed")])
pending = len([t for t in st.session_state["tasks"] if not t.get("completed")])
level = xp // 100 + 1

st.header("🎮 Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Level", level)
col2.metric("XP", xp)
col3.metric("Pending", pending)

progress = min(1.0, xp / 500)
st.progress(progress)
st.caption(f"🌱 Calm · Focused · Rewarding — Level {level}")

# XP badges
if xp < 200:
    st.info("🏅 Badge: Focus Rookie — Keep going!")
elif xp < 400:
    st.success("🎯 Badge: Flow Seeker — You’re improving fast!")
else:
    st.balloons()
    st.success("🧠 Badge: Master of Momentum — Top performer!")

st.markdown("<center><small>Built by <b>Shafail Siddiqha</b> for Persist Ventures AI Assignment</small></center>", unsafe_allow_html=True)
