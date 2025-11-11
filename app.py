import streamlit as st
import json, os, random, matplotlib.pyplot as plt

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="PersistAI – ADHD Flow MVP", page_icon="⚡", layout="centered")

# ---------- GLOBAL THEME (with mobile responsiveness) ----------
st.markdown("""
<style>
/* 🌟 Mobile & Desktop Responsive Design for PersistAI */
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

/* ---------- MOBILE OPTIMIZATION ---------- */
@media only screen and (max-width: 768px) {
    [data-testid="stAppViewContainer"] { padding: 0.8rem !important; }
    h1, h2, h3 { text-align: center !important; font-size: 1.25rem !important; }
    .stButton>button { width: 100% !important; font-size: 0.95rem !important; border-radius: 12px !important; padding: 0.6rem !important; }
    [data-testid="stMetric"] { display: block !important; text-align: center !important; margin: 0.6rem 0 !important; }
    [data-testid="stMetricValue"] { font-size: 1.1rem !important; color: #f28b82 !important; }
    [data-testid="stSidebar"] { width: 230px !important; font-size: 0.9rem !important; padding: 0.5rem !important; }
    div.stAlert { text-align: center !important; font-size: 0.9rem !important; border-radius: 12px !important; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0.5rem !important; }
    footer { text-align: center !important; font-size: 0.8rem !important; }
}
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
    ## ⚡ **PersistAI — ADHD Flow MVP**
    A Smart Multi-Agent Productivity System inspired by ADHD neuroscience and energy management.
    
    PersistAI helps users with **attention variability** stay in productive “flow states” by adapting tasks, moods, and focus patterns dynamically through **specialized child agents**.
    
    ---

    ### 🧭 **Core Philosophy**
    - 🌊 *Flow Over Force* — work with your rhythm, not against it  
    - 💫 *Progress > Perfection* — celebrate consistent effort  
    - 🔁 *Energy-Aware Planning* — tasks adapt to your focus & fatigue  
    - 🧩 *Modular Intelligence* — each “agent” performs one job well  
    - 🌱 *Gentle Gamification* — earn XP for calm, sustainable productivity  
    
    ---

    ### 🤖 **Agent Ecosystem**
    | Agent | Function | Symbol |
    |:------|:----------|:------:|
    | 🧩 **Tasks Manager** | Add, complete, and earn XP through consistent progress | ✅ |
    | 📊 **Weekly Report** | Visual progress tracking & task analytics | 📈 |
    | 🌐 **Browse Agent** | Curated productivity content & ADHD-friendly resources | 🔍 |
    | 🎧 **Focus Companion** | Pomodoro sessions with ambient sound & loop sync | 🎵 |
    | 😊 **Mood Agent** | Track emotions and reflections to understand patterns | 💭 |
    | 💡 **Idea Agent** | Capture spontaneous thoughts via text or voice | 🗣️ |
    
    ---

    ### 👩‍💻 **Built By**
    **Shafail Siddiqha**  
    for **Persist Ventures AI Engineer Assingment (MVP Stage)**  
    _“Consistency over intensity — one task, one flow at a time.”_ 🌻
    """)


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

