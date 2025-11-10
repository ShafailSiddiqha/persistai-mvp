import streamlit as st
# ---------- Aesthetic Global Theme ----------
st.markdown("""
<style>
/* Main background with gentle gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
    color: #2B2B2B;
    font-family: 'Poppins', sans-serif;
}

/* Sidebar with pastel tint */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f3e8ff 0%, #e0f7ff 100%);
    border-right: 1px solid #E2E8F0;
}

/* Headings */
h1, h2, h3 {
    color: #6246EA; /* violet accent */
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #96CDFB, #F5C2E7);
    color: #1E1E2E;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 10px rgba(100, 100, 150, 0.2);
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Sliders */
[data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(90deg, #89b4fa, #f5c2e7);
}

/* Metric boxes */
[data-testid="stMetricValue"] {
    color: #f28b82 !important;
}

/* Progress bar */
[data-testid="stProgressBar"] div div {
    background: linear-gradient(90deg,#96CDFB,#F5C2E7);
}

/* Info boxes */
div.stAlert {
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(100,100,150,0.1);
}

/* Divider line */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #f5c2e7, #96cdfb);
    border-radius: 2px;
}

/* Footer */
footer, .css-164nlkn {
    color: #6B7280;
    text-align: center;
}

/* Smooth animation */
*, *:before, *:after {
    transition: all 0.3s ease-in-out;
}
</style>
""", unsafe_allow_html=True)


import json, os

st.set_page_config(page_title="PersistAI – ADHD Flow MVP", page_icon="⚡", layout="centered")

# Load and save functions
DATA_FILE = "data.json"
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"tasks": [], "xp": 0}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

data = load_data()

# ---- HEADER ----
st.title("⚡ PersistAI – ADHD Flow MVP")
st.caption("Smart Parent–Child Agent System | ADHD Flow | XP Gamification")

# ---- ENERGY LEVEL SLIDER ----
st.subheader("How energetic do you feel today?")
energy = st.slider("Energy Level", 0, 100, 60, help="Adjust based on your current focus and motivation level")

# Feedback message that changes based on slider
if energy < 40:
    st.warning("Low energy 💤 — focus on simple or creative tasks.")
elif energy < 70:
    st.info("Moderate energy ⚙️ — medium tasks are fine.")
else:
    st.success("High energy ⚡ — take on challenging tasks!")

st.divider()

# ---- DASHBOARD ----
st.header("🎮 Dashboard")

xp = data.get("xp", 0)
total_tasks = len(data["tasks"])
completed = len([t for t in data["tasks"] if t.get("done")])
level = xp // 100 + 1

col1, col2, col3 = st.columns(3)
col1.metric("Level", level)
col2.metric("XP", xp)
col3.metric("Tasks Done", completed)

st.progress(min(1.0, xp / 500))
st.caption("🌱 Calm · Focused · Rewarding — Built for ADHD Flow")

st.divider()

# ---- FOOTER ----
st.markdown("<center><small>Built by <b>Shafail Siddiqha</b> for Persist Ventures AI Challenge</small></center>", unsafe_allow_html=True)
