import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tasks Manager", page_icon="🧩", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
/*  Mobile & Desktop Responsive Design for PersistAI */

/* Default desktop/laptop view remains unchanged */

/*  Mobile optimization for width < 768px */
@media only screen and (max-width: 768px) {

    /* Reduce global padding */
    [data-testid="stAppViewContainer"] {
        padding: 0.8rem !important;
    }

    /* Center headings and slightly reduce size */
    h1, h2, h3 {
        text-align: center !important;
        font-size: 1.25rem !important;
    }

    /* Make buttons easy to tap */
    .stButton>button {
        width: 100% !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.6rem !important;
    }

    /* Adjust text fields and sliders */
    input, .stSlider {
        font-size: 0.9rem !important;
    }

    /* Stack metrics vertically for clarity */
    [data-testid="stMetric"] {
        display: block !important;
        text-align: center !important;
        margin: 0.6rem 0 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
        color: #f28b82 !important;
    }

    /* Compact sidebar for mobile */
    [data-testid="stSidebar"] {
        width: 230px !important;
        font-size: 0.9rem !important;
        padding: 0.5rem !important;
        background: linear-gradient(180deg, #f3e8ff 0%, #e0f7ff 100%) !important;
    }

    /* Center info and alert boxes */
    div.stAlert {
        text-align: center !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
    }

    /* Reduce vertical spacing between sections */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* Center footer text */
    footer {
        text-align: center !important;
        font-size: 0.8rem !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "xp" not in st.session_state:
    st.session_state["xp"] = 0

# ---------- FUNCTIONS ----------
def add_task(title, difficulty):
    task = {
        "id": int(datetime.utcnow().timestamp()),
        "title": title,
        "difficulty": difficulty,
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    st.session_state["tasks"].append(task)

def mark_done(task_id):
    for t in st.session_state["tasks"]:
        if t["id"] == task_id and not t["completed"]:
            t["completed"] = True
            t["completed_at"] = datetime.utcnow().isoformat()
            xp_gain = 10 * t["difficulty"]
            st.session_state["xp"] += xp_gain
            st.toast(f"🎮 +{xp_gain} XP gained!")

def delete_task(task_id):
    st.session_state["tasks"] = [t for t in st.session_state["tasks"] if t["id"] != task_id]

# ---------- UI ----------
st.title("🧩 Tasks Manager")
st.caption("Add, complete, or delete your tasks to stay in flow.")

with st.form("add_task_form", clear_on_submit=True):
    title = st.text_input("Task title")
    difficulty = st.slider("Difficulty (1 easy → 3 hard)", 1, 3, 1)
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if title.strip():
            add_task(title, difficulty)
            st.success(f"Added: {title}")
            st.rerun()
        else:
            st.warning("Please enter a task name.")

st.markdown("---")
st.subheader("Your Tasks")

if not st.session_state["tasks"]:
    st.info("No tasks added yet.")
else:
    for t in sorted(st.session_state["tasks"], key=lambda x: x["created_at"], reverse=True):
        cols = st.columns([6, 1, 1])
        with cols[0]:
            icon = "✅" if t["completed"] else "⏳"
            st.write(f"**{t['title']}** — Difficulty {t['difficulty']} {icon}")
        with cols[1]:
            if not t["completed"]:
                if st.button("Done", key=f"done_{t['id']}"):
                    mark_done(t["id"])
                    st.rerun()
        with cols[2]:
            if st.button("❌", key=f"del_{t['id']}"):
                delete_task(t["id"])
                st.rerun()


