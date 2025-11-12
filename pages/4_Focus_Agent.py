import streamlit as st
import time
import random
import base64

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Focus Companion Agent", page_icon="🎧", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
    color: #2B2B2B;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f3e8ff 0%, #e0f7ff 100%);
    border-right: 1px solid #E2E8F0;
}
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

@media only screen and (max-width: 768px) {
    h1, h2, h3 { text-align: center !important; font-size: 1.25rem !important; }
    .stButton>button { width: 100% !important; padding: 0.6rem !important; font-size: 0.95rem !important; }
    [data-testid="stMetric"] { display: block !important; text-align: center !important; margin: 0.6rem 0 !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "xp" not in st.session_state:
    st.session_state["xp"] = 0
if "focus_active" not in st.session_state:
    st.session_state["focus_active"] = False
if "audio_started" not in st.session_state:
    st.session_state["audio_started"] = False

# ---------- HEADER ----------
st.title("🎧 Focus Companion Agent")
st.caption("Pomodoro • Ambient Sound • ADHD Flow Optimizer 🌿")

# ---------- SOUND OPTIONS ----------
st.subheader("🎵 Choose your ambient sound")

sound_links = {
    "Rain": "rain.mp3",
    "Ocean Waves": "ocean.mp3",
    "Bird Chirping": "bird.mp3",
    "Focus Music": "focus.mp3"
}

sound_choice = st.radio("Pick a sound:", list(sound_links.keys()), horizontal=True)
loop_mode = st.toggle("🔁 Loop Mode (auto-restart every 25 min)", value=True)
duration = st.slider("Focus session duration (minutes)", 5, 60, 25)

# ---------- START BUTTON ----------
if st.button("▶️ Start Focus Session"):
    st.session_state["focus_start"] = time.time()
    st.session_state["focus_duration"] = duration * 60
    st.session_state["sound_choice"] = sound_choice
    st.session_state["focus_active"] = True
    st.session_state["audio_started"] = False
    st.success(f"🧘 Focus session started with {sound_choice} sound")
    st.rerun()

# ---------- TIMER ----------
if st.session_state.get("focus_active", False):
    elapsed = time.time() - st.session_state["focus_start"]
    remaining = st.session_state["focus_duration"] - elapsed
    progress = max(0, min(1, 1 - (elapsed / st.session_state["focus_duration"])))
    minutes_left = int(remaining // 60)
    seconds_left = int(remaining % 60)

    st.progress(progress)
    st.metric("⏳ Time Remaining", f"{minutes_left:02d}:{seconds_left:02d}")

    # ---------- AUDIO PLAYBACK WITH STREAMLIT'S NATIVE PLAYER ----------
    sound_file = sound_links[st.session_state["sound_choice"]]
    
    # Try to play audio using Streamlit's audio player
    try:
        import os
        if os.path.exists(sound_file):
            st.audio(sound_file, format="audio/mp3", loop=True)
        else:
            st.warning(f"⚠️ Audio file '{sound_file}' not found. Please ensure MP3 files are in the app directory.")
    except Exception as e:
        st.error(f"Audio playback error: {str(e)}")
    
    st.caption("🔊 Use the play button above to start the ambient sound")

    # ---------- STOP BUTTON ----------
    if st.button("⏹ Stop Session"):
        st.session_state["focus_active"] = False
        st.info("Session ended early. Take a short break 🌿")
        st.rerun()

    # Auto-rerun every second to update timer
    time.sleep(1)
    st.rerun()

    # ---------- SESSION END ----------
    if remaining <= 0:
        st.session_state["focus_active"] = False
        st.balloons()
        xp_gain = 20
        st.session_state["xp"] += xp_gain
        st.success(f"🎯 Focus session complete! +{xp_gain} XP earned 💪")

        if loop_mode:
            st.info("🔁 Loop Mode active — restarting next Pomodoro...")
            time.sleep(3)
            st.session_state["focus_start"] = time.time()
            st.session_state["focus_active"] = True
            st.rerun()

# ---------- REWARD MESSAGE ----------
if not st.session_state.get("focus_active", False) and "focus_start" in st.session_state:
    st.markdown("---")
    rewards = [
        "✨ You focused like a pro!",
        "💪 Great session — stay in flow!",
        "🌻 Calm mind, strong focus.",
        "🎶 You're building consistency.",
        "🧠 Another step toward mastery!"
    ]
    st.success(random.choice(rewards))
    st.metric("🏆 Total XP", st.session_state["xp"])
    
