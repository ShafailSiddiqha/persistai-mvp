# pages/1_Tasks_Manager.py — Tasks Manager page
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
from datetime import datetime

st.set_page_config(page_title="Tasks Manager", page_icon="🧩", layout="centered")

DATA_FILE = "data.json"
def load_data():
    if not os.path.exists(DATA_FILE):
        default = {"tasks": [], "xp": 0}
        with open(DATA_FILE, "w") as f: json.dump(default, f)
        return default
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=2)

def task_agent_create(title, data, difficulty=1):
    task = {
        "id": int(datetime.utcnow().timestamp()),
        "title": title,
        "created_at": datetime.utcnow().isoformat(),
        "done": False,
        "difficulty": difficulty
    }
    data["tasks"].append(task)
    save_data(data)
    return task

def task_agent_mark_done(task_id, data):
    for t in data["tasks"]:
        if t["id"] == task_id and not t["done"]:
            t["done"] = True
            t["completed_at"] = datetime.utcnow().isoformat()
            save_data(data)
            return t
    return None

def xp_agent_award_for_task(task, data):
    base = 10
    xp_gain = base * task.get("difficulty", 1)
    data["xp"] = data.get("xp", 0) + xp_gain
    save_data(data)
    return xp_gain

data = load_data()

st.title("🧩 Tasks Manager")
st.write("Add tasks, mark done, and earn XP.")

with st.form("add_task", clear_on_submit=True):
    task_text = st.text_input("Task title (e.g., 'Write report')", "")
    difficulty = st.slider("Difficulty (1 easy → 3 hard)", 1, 3, 1)
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if not task_text.strip():
            st.warning("Please enter a task title.")
        else:
            created = task_agent_create(task_text.strip(), data, difficulty)
            st.success(f"Task added: {created['title']} (difficulty {created['difficulty']})")
            st.rerun()


st.markdown("---")
st.subheader("Your Tasks")

if not data["tasks"]:
    st.info("No tasks yet. Add one above!")
else:
    for t in sorted(data["tasks"], key=lambda x: x["created_at"], reverse=True):
        cols = st.columns([6, 1, 1])
        with cols[0]:
            status = "✅" if t.get("done") else "⏳"
            st.write(f"**{t['title']}** — Difficulty: {t.get('difficulty')} {status}")
            if t.get("done"):
                st.caption(f"Completed at: {t.get('completed_at')}")
            else:
                st.caption(f"Created at: {t.get('created_at')}")
        with cols[1]:
            if not t.get("done"):
                if st.button("Mark Done", key=f"done_{t['id']}"):
                    done_task = task_agent_mark_done(t["id"], data)
                    xp = xp_agent_award_for_task(done_task, data)
                    st.toast(f"Awarded +{xp} XP!", icon="🎮")
                    st.rerun()

        with cols[2]:
            if st.button("Delete", key=f"del_{t['id']}"):
                data["tasks"] = [x for x in data["tasks"] if x["id"] != t["id"]]
                save_data(data)
                st.info("Deleted task.")
                st.rerun()

