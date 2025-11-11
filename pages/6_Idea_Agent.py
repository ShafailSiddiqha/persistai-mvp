import streamlit as st
import json, os
from datetime import datetime
import whisper

st.set_page_config(page_title="Idea Agent", page_icon="💡", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#FAF8FF 0%,#FDFBFF 100%);
    color:#2B2B2B; font-family:'Poppins',sans-serif;
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
st.caption("Capture or speak your spontaneous thoughts — before they vanish!")

# ---------- TEXT INPUT ----------
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
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "text"
        }
        st.session_state["ideas"].append(idea)
        save_data(st.session_state["ideas"])
        st.success("✅ Idea saved successfully!")
        st.rerun()
    else:
        st.warning("Type something before saving!")

st.divider()

# ---------- VOICE CAPTURE ----------
st.subheader("🎙️ Voice Capture")
st.markdown("<small>Record your voice instantly if typing feels slow!</small>", unsafe_allow_html=True)

try:
    from streamlit_mic_recorder import mic_recorder

    audio = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording", key="recorder")

    if audio:
        file_name = f"idea_{datetime.now().strftime('%H%M%S')}.wav"
        with open(file_name, "wb") as f:
            f.write(audio["bytes"])
        st.audio(file_name)
        st.success(f"✅ Voice idea saved as {file_name}")

        st.session_state["ideas"].append({
            "text": file_name,
            "category": "Voice Recording",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "audio"
        })
        save_data(st.session_state["ideas"])
        st.rerun()

except Exception as e:
    st.warning("⚠️ Voice recording requires 'streamlit-mic-recorder'. Add it to requirements.txt if not installed.")
    st.code("pip install streamlit-mic-recorder")

st.divider()

# ---------- DISPLAY SAVED IDEAS ----------
st.subheader("🗂️ Saved Ideas")

if not st.session_state["ideas"]:
    st.info("No ideas captured yet.")
else:
    for idx, idea in enumerate(reversed(st.session_state["ideas"]), 1):
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            if idea["type"] == "text":
                st.markdown(f"**{idx}. {idea['text']}**")
                st.caption(f"🕒 {idea['timestamp']} | 📁 {idea['category']}")
            else:
                st.markdown(f"🎧 Voice Idea {idx}")
                st.audio(idea["text"])
                st.caption(f"🕒 {idea['timestamp']}")

        with col2:
            if idea["type"] == "audio":
                if st.button("🗣️ Transcribe", key=f"trans_{idx}"):
                    try:
                        model = whisper.load_model("tiny")
                        result = model.transcribe(idea["text"])
                        st.session_state["ideas"].append({
                            "text": result["text"],
                            "category": "Transcribed",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "type": "text"
                        })
                        save_data(st.session_state["ideas"])
                        st.success("✅ Transcription complete!")
                        st.rerun()
                    except Exception as e:
                        st.error("❌ Transcription failed. Ensure openai-whisper is installed.")
                        st.write(str(e))

        with col3:
            if st.button("🗑️", key=f"delete_{idx}"):
                st.session_state["ideas"].remove(idea)
                save_data(st.session_state["ideas"])
                st.success("🗑️ Idea deleted.")
                st.rerun()

st.caption("💡 Idea Agent — capture, listen, and even transcribe your creative sparks effortlessly.")
