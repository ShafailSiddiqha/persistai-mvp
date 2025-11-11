# pages/4_Focus_Agent.py
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Focus Agent", page_icon="⏱️", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg,#FAF8FF 0%,#FDFBFF 100%); font-family: 'Poppins', sans-serif; color:#222;}
h1,h2,h3 { color:#5A3EBA; }
.stButton>button { background: linear-gradient(90deg,#A1C4FD,#C2E9FB); color:#1E1E2E; border-radius:10px; }
@media only screen and (max-width:768px) { h1,h2,h3 { text-align:center; } .stButton>button{width:100%!important;} }
</style>
""", unsafe_allow_html=True)

if "focus_running" not in st.session_state:
    st.session_state["focus_running"] = False
if "focus_end" not in st.session_state:
    st.session_state["focus_end"] = None
if "focus_duration" not in st.session_state:
    st.session_state["focus_duration"] = 25  # minutes default
if "xp" not in st.session_state:
    st.session_state["xp"] = 0

st.title("⏱️ Focus Agent")
st.caption("Start a focused session. Complete it to earn a small XP bonus.")

dur = st.selectbox("Session length (minutes)", [15, 20, 25, 30, 45], index=2)
st.session_state["focus_duration"] = dur

cols = st.columns([2,2,2])
with cols[0]:
    if st.button("Start Focus Session"):
        st.session_state["focus_running"] = True
        st.session_state["focus_end"] = datetime.utcnow() + timedelta(minutes=st.session_state["focus_duration"])
        st.success(f"Focus session started for {st.session_state['focus_duration']} minutes.")
        st.experimental_rerun()
with cols[1]:
    if st.button("Cancel Session"):
        st.session_state["focus_running"] = False
        st.session_state["focus_end"] = None
        st.info("Focus session canceled.")
with cols[2]:
    if st.button("Claim Bonus (if finished)"):
        if st.session_state.get("focus_running") and st.session_state.get("focus_end"):
            if datetime.utcnow() >= st.session_state["focus_end"]:
                bonus = 5  # small XP bonus
                st.session_state["xp"] += bonus
                st.session_state["focus_running"] = False
                st.session_state["focus_end"] = None
                st.success(f"Well done! +{bonus} XP awarded.")
            else:
                remaining = st.session_state["focus_end"] - datetime.utcnow()
                st.warning(f"Session not finished — {remaining.seconds//60}m {remaining.seconds%60}s left.")
        else:
            st.info("No active session to claim.")

st.markdown("---")
if st.session_state.get("focus_running") and st.session_state.get("focus_end"):
    remaining = st.session_state["focus_end"] - datetime.utcnow()
    if remaining.total_seconds() > 0:
        mins = remaining.seconds // 60
        secs = remaining.seconds % 60
        st.metric("Time left", f"{mins}m {secs}s")
    else:
        st.success("Focus session ended — you can claim your bonus!")
else:
    st.info("No active focus session. Start one to build momentum.")

st.markdown("---")
st.info("Focus Agent simulates a child agent that helps you build flow using focused sessions.")
