# pages/9_Focus_Companion.py
import streamlit as st
from datetime import datetime, timedelta
import random
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Focus Companion Agent", page_icon="🎧", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#FAF8FF 0%,#FDFBFF 100%);
    color:#2B2B2B;
    font-family:'Poppins',sans-serif;
}
h1,h2,h3 { color:#5A3EBA; text-align:center; }
.stButton>button {
    background: linear-gradient(90deg,#A1C4FD,#C2E9FB);
    color:#1E1E2E; border:none; border-radius:10px;
    font-weight:600; box-shadow:0 4px 10px rgba(150,150,200,0.2);
}
.stButton>button:hover { transform:scale(1.05); }
@media only screen and (max-width:768px){
    h1,h2,h3{text-align:center;}
    .stButton>button{width:100%!important;}
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "focus_running" not in st.session_state:
    st.session_state["focus_running"] = False
if "focus_end" not in st.session_state:
    st.session_state["focus_end"] = None
if "xp" not in st.session_state:
    st.session_state["xp"] = 0
if "sound" not in st.session_state:
    st.session_state["sound"] = "None"
if "loop_mode" not in st.session_state:
    st.session_state["loop_mode"] = False

# ---------- HEADER ----------
st.title("🎧 Focus Companion Agent")
st.caption("Pomodoro focus + ambient environment + motivation system for ADHD flow.")

# ---------- SOUND COMPANION ----------
st.subheader("🌈 Choose your focus soundscape")
sound = st.radio(
    "Pick an ambient sound to play during your session:",
    ["None", "Rain", "Ocean Waves", "Cafe Ambience", "Focus Music"]
)
st.session_state["sound"] = sound

# Ambient sound URLs (free & Streamlit-safe)
sound_links = {
    "Rain": "https://cdn.pixabay.com/audio/2021/11/09/audio_14c76ba1ff.mp3",
    "Ocean Waves": "https://cdn.pixabay.com/audio/2022/03/15/audio_5d1cf13a22.mp3",
    "Cafe Ambience": "https://cdn.pixabay.com/audio/2022/02/17/audio_2f8cfc36a4.mp3",
    "Focus Music": "https://cdn.pixabay.com/audio/2022/03/10/audio_4c1f63e2d3.mp3"
}

# Loop mode toggle
st.session_state["loop_mode"] = st.checkbox("🔁 Loop Mode (Restart sound every 25 min)", value=False)

if sound != "None":
    st.audio(sound_links[sound], format="audio/mp3")

st.divider()

# ---------- FOCUS TIMER ----------
dur = st.selectbox("🎯 Focus session length (minutes)", [15, 20, 25, 30, 45], index=2)
cols = st.columns([2,2,2])
with cols[0]:
    if st.button("▶️ Start Focus"):
        st.session_state["focus_running"] = True
        st.session_state["focus_end"] = datetime.utcnow() + timedelta(minutes=dur)
        st.success(f"Focus session started for {dur} minutes.")
        st.experimental_rerun()
with cols[1]:
    if st.button("⏹️ Stop"):
        st.session_state["focus_running"] = False
        st.session_state["focus_end"] = None
        st.info("Session stopped.")
with cols[2]:
    if st.button("🏆 Claim XP"):
        if st.session_state.get("focus_end") and datetime.utcnow() >= st.session_state["focus_end"]:
            bonus = 5
            st.session_state["xp"] += bonus
            st.success(f"🎉 Great focus! +{bonus} XP added.")
            st.session_state["focus_running"] = False
            st.session_state["focus_end"] = None
        else:
            st.warning("⏳ Session not complete yet.")

st.divider()

# ---------- LIVE SESSION ----------
if st.session_state["focus_running"] and st.session_state["focus_end"]:
    remaining = st.session_state["focus_end"] - datetime.utcnow()
    if remaining.total_seconds() > 0:
        mins = remaining.seconds // 60
        secs = remaining.seconds % 60
        st.metric("Time Remaining", f"{mins:02d}:{secs:02d}")

        # Affirmations
        affirmations = [
            "🌱 Stay calm — steady focus builds results.",
            "🔥 One step at a time — you’re doing great!",
            "💡 Progress, not perfection.",
            "🎯 Breathe, refocus, flow continues.",
            "💪 You’ve got this!"
        ]
        if random.randint(0, 100) < 8:
            st.info(random.choice(affirmations))

        # Loop Mode: restart sound if 25 min passed
        if st.session_state["loop_mode"]:
            elapsed = dur - mins
            if elapsed >= 25 and sound != "None":
                st.audio(sound_links[sound], format="audio/mp3")
                st.toast("🔁 Loop mode: Ambient restarted", icon="🎵")

    else:
        st.success("⏰ Focus session complete! Claim your XP bonus above.")
else:
    st.info("Start a focus session to activate your ambient companion.")

st.markdown("---")
st.caption("🧘 Focus Companion Agent syncs your environment and energy to help ADHD brains stay calm, consistent, and rewarded.")
