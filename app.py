import streamlit as st
import json, os, random, matplotlib.pyplot as plt

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="PersistAI – ADHD Flow MVP", page_icon="⚡", layout="centered")

/*  Mobile & Desktop Responsive Design for PersistAI */

/* Default desktop/laptop view remains unchanged */

/*  Mobile optimization for width < 768px */
@media only screen and (max-width: 768px) {

    /* Reduce global padding */
    [data-testid="stAppViewContainer"] {
        padding: 0.8rem !important;
    }

    /* Center headings and slightly reduce size */
    h1, h2, h3 {
        text-align: center !important;
        font-size: 1.25rem !important;
    }

    /* Make buttons easy to tap */
    .stButton>button {
        width: 100% !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.6rem !important;
    }

    /* Adjust text fields and sliders */
    input, .stSlider {
        font-size: 0.9rem !important;
    }

    /* Stack metrics vertically for clarity */
    [data-testid="stMetric"] {
        display: block !important;
        text-align: center !important;
        margin: 0.6rem 0 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
        color: #f28b82 !important;
    }

    /* Compact sidebar for mobile */
    [data-testid="stSidebar"] {
        width: 230px !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        background: linear-gradient(180deg, #f3e8ff 0%, #e0f7ff 100%) !important;
    }

    /* Center info and alert boxes */
    div.stAlert {
        text-align: center !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
    }

    /* Reduce vertical spacing between sections */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* Center footer text */
    footer {
        text-align: center !important;
        font-size: 0.8rem !important;
    }
}


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


