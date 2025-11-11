# pages/10_Idea_Agent.py
import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Idea Agent", page_icon="💡", layout="centered")

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

# ---------- SESSION ----------
if "ideas" not in st.session_state:
    st.session_state["ideas"] = []

# ---------- FILE ----------
DATA_FILE = "ideas.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- HEADER ----------
st.title("💡 Idea Agent")
st.caption("Capture your spontaneous thoughts — before they vanish!")

# ---------- INPUT ----------
st.subheader("✏️ Quick Capture")
col1, col2 = st.columns([3, 1])
with col1:
    idea_text = st.text_input("Write your idea or thought...", placeholder="E.g. New app feature, blog title, project insight...")
with col2:
    category = st.selectbox("Category", ["Work", "Study", "Personal", "Other"])

if st.button("💾 Save Idea"):
    if idea_text.strip():
        idea = {
            "text": idea_text.strip(),
            "category": category,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state["ideas"].append(idea)
        save_data(st.session_state["ideas"])
        st.success("✅ Idea saved successfully!")
    else:
        st.warning("Type something before saving!")

st.divider()

# ---------- VOICE RECORDER ----------
st.subheader("🎙️ Voice Capture (Beta Feature)")

st.markdown("""
<small>Sometimes thoughts appear faster than typing — record your idea instantly!</small>
""", unsafe_allow_html=True)

# Use Streamlit's built-in audio recorder (Community Component)
try:
    from streamlit_mic_recorder import mic_recorder, speech_to_text
    st.info("🎧 Click below to record your voice. Press stop when done.")
    audio = mic_recorder(start_prompt="🎙️ Record Idea", stop_prompt="⏹️ Stop", key="recorder")

    if audio:
        file_name = f"idea_{datetime.now().strftime('%H%M%S')}.wav"
        with open(file_name, "wb") as f:
            f.write(audio["bytes"])
        st.success(f"✅ Voice idea saved as {file_name}")
        st.audio(file_name)
except Exception:
    st.warning("⚠️ Voice recording requires the `streamlit-mic-recorder` package. You can install it with: `pip install streamlit-mic-recorder`")

st.divider()

# ---------- DISPLAY SAVED IDEAS ----------
st.subheader("🗂️ Saved Ideas")
if not st.session_state["ideas"]:
    st.info("No ideas captured yet.")
else:
    for i, idea in enumerate(reversed(st.session_state["ideas"][-10:]), 1):
        st.markdown(f"**{i}. {idea['text']}**")
        st.caption(f"🕒 {idea['timestamp']} | 📁 {idea['category']}")
        st.markdown("---")

st.caption("💡 Idea Agent helps ADHD users instantly record creative sparks — typed or spoken — before they fade away.")
