import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tasks Manager", page_icon="🧩", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FDFBFF 0%, #FAF7FF 100%);
    font-family: 'Poppins', sans-serif;
    color: #222;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
}
h1, h2, h3 { color: #5A3EBA; font-weight: 700; }
.stButton>button {
    background: linear-gradient(90deg, #A1C4FD, #C2E9FB);
    color: #1E1E2E;
    border-radius: 10px;
    border: none;
    padding: 0.3rem 0.8rem;
    box-shadow: 0 3px 10px rgba(120,120,160,0.2);
}
.stButton>button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "xp" not in st.session_state:
    st.session_state["xp"] = 0

# ---------- HELPERS ----------
def add_task(title, difficulty):
    t = {
        "id": int(datetime.utcnow().timestamp()),
        "title": title,
        "difficulty": difficulty,
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    st.session_state["tasks"].append(t)

def mark_done(task_id):
    for t in st.session_state["tasks"]:
        if t["id"] == task_id and not t["completed"]:
            t["completed"] = True
            t["completed_at"] = datetime.utcnow().isoformat()
            xp_gain = 10 * t["difficulty"]
            st.session_state["xp"] += xp_gain
            st.toast(f"🎮 +{xp_gain} XP gained!")
            return

def delete_task(task_id):
    st.session_state["tasks"] = [t for t in st.session_state["tasks"] if t["id"] != task_id]

# ---------- UI ----------
st.title("🧩 Tasks Manager")
st.caption("Add, complete, or delete tasks to track your daily flow.")

with st.form("add_task_form", clear_on_submit=True):
    title = st.text_input("Task name")
    difficulty = st.slider("Difficulty (1 easy → 3 hard)", 1, 3, 1)
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if title.strip():
            add_task(title, difficulty)
            st.success(f"Task added: {title}")
            st.rerun()
        else:
            st.warning("Please enter a valid task name.")

st.divider()
st.subheader("Your Tasks")

if not st.session_state["tasks"]:
    st.info("No tasks added yet.")
else:
    for t in sorted(st.session_state["tasks"], key=lambda x: x["created_at"], reverse=True):
        cols = st.columns([6, 1, 1])
        with cols[0]:
            icon = "✅" if t["completed"] else "⏳"
            st.write(f"**{t['title']}** — Difficulty: {t['difficulty']} {icon}")
        with cols[1]:
            if not t["completed"]:
                if st.button("Done", key=f"done_{t['id']}"):
                    mark_done(t["id"])
                    st.rerun()
        with cols[2]:
            if st.button("❌", key=f"del_{t['id']}"):
                delete_task(t["id"])
                st.rerun()
