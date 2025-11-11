import streamlit as st
from datetime import datetime
import json, os

st.set_page_config(page_title="Mood Agent", page_icon="😊", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
/* Mobile & Desktop Responsive Design for PersistAI */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
    color: #2B2B2B;
    font-family: 'Poppins', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f3e8ff 0%, #e0f7ff 100%);
    border-right: 1px solid #E2E8F0;
}

h1, h2, h3 { color: #6246EA; }

.stButton>button {
    background: linear-gradient(90deg, #96CDFB, #F5C2E7);
    color: #1E1E2E;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 10px rgba(100, 100, 150, 0.2);
    transition: 0.2s ease-in-out;
}
.stButton>button:hover { transform: scale(1.05); }

div.stAlert {
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(100,100,150,0.1);
}

@media only screen and (max-width: 768px) {
    [data-testid="stAppViewContainer"] { padding: 0.8rem !important; }
    h1, h2, h3 { text-align: center; font-size: 1.2rem !important; }
    .stButton>button { width: 100%; font-size: 0.9rem !important; }
    footer { text-align: center !important; font-size: 0.8rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA HANDLING ----------
DATA_FILE = "mood_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize session
if "mood_logs" not in st.session_state:
    st.session_state["mood_logs"] = load_data()

# ---------- HEADER ----------
st.title("😊 Mood Agent")
st.caption("Track how you feel — quick mood picks and reflections to help the system learn your patterns.")

# ---------- MOOD SELECTION ----------
st.subheader("How do you feel right now?")
mood_options = {
    "😀": "Good",
    "🙂": "Okay",
    "😐": "Distracted",
    "😔": "Overwhelmed"
}
selected_mood = st.radio("Select Mood", list(mood_options.keys()), horizontal=True)
reflection = st.text_area("Short reflection (optional, 1–2 lines)", placeholder="Describe your feeling briefly...")

# ---------- LOG MOOD ----------
if st.button("Log Mood"):
    if selected_mood:
        entry = {
            "mood": selected_mood,
            "note": reflection,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state["mood_logs"].append(entry)
        save_data(st.session_state["mood_logs"])

        st.success("Mood logged ✅")
        st.toast("🧠 Mood saved successfully!")
    else:
        st.warning("Please select a mood first!")

st.divider()

# ---------- FEEDBACK ----------
if st.session_state["mood_logs"]:
    last_mood = st.session_state["mood_logs"][-1]["mood"]
    feedback = {
        "😀": "Keep the positive energy flowing 🌞",
        "🙂": "Nice! Maybe plan something relaxing 🎧",
        "😐": "Take a short break, hydrate 💧",
        "😔": "You’re doing great — rest if needed 💛"
    }
    st.info(f"💬 {feedback.get(last_mood, 'Stay balanced 🌿')}")

st.divider()

# ---------- MOOD HISTORY ----------
st.subheader("📜 Mood History (Recent)")
if st.session_state["mood_logs"]:
    for entry in reversed(st.session_state["mood_logs"][-10:]):  # show latest 10
        st.markdown(f"""
        <div style='background: #f9faff; border-radius: 10px; padding: 10px; margin-bottom: 8px;
                    box-shadow: 0 2px 6px rgba(120,120,180,0.1);'>
            <b style='font-size: 1.1rem;'>{entry["mood"]}</b> 
            <span style='color: gray; font-size: 0.8rem;'>({entry["timestamp"]})</span><br>
            <i>{entry["note"] if entry["note"] else "No reflection added"}</i>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No mood entries yet. Log your first one above!")

st.markdown("<center><small>Built by <b>Shafail Siddiqha</b> for Persist Ventures AI Challenge</small></center>", unsafe_allow_html=True)
