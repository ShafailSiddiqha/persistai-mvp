# pages/5_Mood_Agent.py
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Mood Agent", page_icon="🙂", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg,#FAF8FF 0%,#FDFBFF 100%); font-family:'Poppins',sans-serif; color:#222; }
h1,h2,h3 { color:#5A3EBA; }
.stButton>button { background: linear-gradient(90deg,#A1C4FD,#C2E9FB); color:#1E1E2E; border-radius:10px; }
@media only screen and (max-width:768px) { h1,h2,h3{text-align:center;} .stButton>button{width:100%!important;} }
</style>
""", unsafe_allow_html=True)

if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

st.title("🙂 Mood Agent")
st.caption("Track how you feel — quick mood picks and short reflections help the system learn patterns.")

mood = st.radio("How do you feel right now?", ["🙂 Good", "😐 Okay", "😕 Distracted", "😫 Overwhelmed"], index=1, horizontal=True)
note = st.text_area("Short reflection (optional, 1–2 lines)", value="", max_chars=200)
if st.button("Log Mood"):
    entry = {
        "mood": mood,
        "note": note.strip(),
        "timestamp": datetime.utcnow().isoformat()
    }
    st.session_state["mood_log"].append(entry)
    st.success("Mood logged ✅")
    st.experimental_rerun()

st.markdown("---")
st.subheader("Recent mood entries")
if st.session_state["mood_log"]:
    for e in reversed(st.session_state["mood_log"][-6:]):
        st.markdown(f"**{e['mood']}** — {e['timestamp']}")
        if e.get("note"):
            st.caption(e["note"])
else:
    st.info("No mood logs yet — log one to start seeing trends.")

st.markdown("---")
st.info("Mood Agent helps capture emotional context — useful for future analytics and ADHD flow tuning.")
