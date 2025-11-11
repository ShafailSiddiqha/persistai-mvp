# pages/3_Browse_Agent.py
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Browse Agent", page_icon="🧭", layout="centered")

# ---------- THEME ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAF8FF 0%, #FDFBFF 100%);
    color: #2B2B2B;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
}
h1, h2, h3 { color: #5A3EBA; font-weight: 700; }
.stButton>button {
    background: linear-gradient(90deg,#A1C4FD,#C2E9FB);
    color: #1E1E2E;
    border-radius: 10px; border: none;
    box-shadow: 0 3px 10px rgba(120,120,160,0.15);
}
@media only screen and (max-width: 768px) {
    h1, h2, h3 { text-align:center; font-size:1.2rem; }
    .stButton>button { width:100% !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "xp" not in st.session_state:
    st.session_state["xp"] = 0
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---------- UI ----------
st.title("🧭 Browse Agent")
st.caption("Smart task suggester — tailored to your energy level and role.")

energy = st.slider("How energetic do you feel?", 0, 100, st.session_state.get("energy", 60))
st.session_state["energy"] = energy
user_type = st.selectbox("Select your role", ["Developer", "Engineer", "Student", "General"], index=0)

# ---------- TASK LIBRARY ----------
suggestions = {
    "Developer": {
        "low": [
            "Refactor one old function",
            "Review a teammate’s code",
            "Read an article on clean code",
            "Document your latest module",
            "Organize your project folders",
            "Test an API endpoint manually",
            "Sketch UI flow on paper",
            "Write pseudocode for next feature",
            "Clean unused imports in your code",
            "Update your README file",
            "Check error logs for warnings",
            "Review recent commits",
            "Rename confusing variables",
            "Backup important scripts",
            "Plan your next coding session"
        ],
        "medium": [
            "Implement one medium-complex feature",
            "Debug and fix known bug",
            "Write 5 unit tests",
            "Improve error handling",
            "Integrate a small API",
            "Enhance UI responsiveness",
            "Work on documentation examples",
            "Optimize a SQL query",
            "Code review + refactor 1 module",
            "Build simple CLI utility",
            "Write helper function for re-use",
            "Check lint warnings and fix",
            "Add comments for clarity",
            "Automate a small repetitive task",
            "Plan tomorrow’s sprint"
        ],
        "high": [
            "Develop a new service end-to-end",
            "Implement authentication flow",
            "Deploy test version on cloud",
            "Design new database schema",
            "Build API integration with OAuth",
            "Solve algorithm challenge",
            "Create automated test pipeline",
            "Implement caching for speed",
            "Refactor architecture layers",
            "Contribute to open-source repo",
            "Design system diagram for docs",
            "Implement CI/CD workflow",
            "Benchmark app performance",
            "Experiment with new library",
            "Code and test for 2 hours straight"
        ]
    },
    "Engineer": {
        "low": [
            "Organize project documentation",
            "Check hardware connections or drawings",
            "Review yesterday’s logs or readings",
            "Clean your workbench or workspace",
            "Backup design files",
            "Send update emails",
            "Sketch design idea",
            "Inspect minor defects",
            "Sort technical references",
            "List pending approvals",
            "Review safety checklist",
            "Verify part numbers",
            "Read about new tools",
            "Label stored materials",
            "Plan maintenance schedule"
        ],
        "medium": [
            "Run diagnostics on subsystem",
            "Calibrate equipment",
            "Simulate design parameters",
            "Prepare technical report",
            "Inspect part or circuit layout",
            "Cross-check BOM list",
            "Collaborate with technician",
            "Review supplier quote",
            "Prepare next-day material list",
            "Update schematic in CAD",
            "Check tolerance limits",
            "Verify calibration data",
            "Draft design proposal",
            "Train junior engineer",
            "Plan resource allocation"
        ],
        "high": [
            "Design new prototype",
            "Run performance tests",
            "Analyze system failure",
            "Implement design changes",
            "Develop automation tool",
            "Prepare design presentation",
            "Review production quality metrics",
            "Integrate new sensor or component",
            "Lead design review meeting",
            "Optimize process efficiency",
            "Simulate extreme condition tests",
            "Finalize project documentation",
            "Design experimental setup",
            "Develop new process workflow",
            "Create cost optimization report"
        ]
    },
    "Student": {
        "low": [
            "Organize your notes",
            "Revise yesterday’s class",
            "Watch an educational video",
            "Summarize one topic",
            "Make flashcards",
            "Plan study schedule",
            "Declutter desk",
            "Review mistakes in last test",
            "Write one paragraph summary",
            "Sort assignments by deadline",
            "Read one textbook page",
            "Ask one question in forum",
            "Rewrite confusing notes",
            "Prepare stationery",
            "Listen to calm focus music"
        ],
        "medium": [
            "Study one chapter",
            "Solve 10 practice problems",
            "Attempt one past-year question",
            "Write notes for upcoming lecture",
            "Group study or discuss topic",
            "Watch concept video and summarize",
            "Take a small quiz",
            "Review 3 key formulas",
            "Highlight textbook sections",
            "Plan revision timetable",
            "Read research article abstract",
            "Summarize lab experiment",
            "Write 5 MCQs for self-quiz",
            "Create mind map of topic",
            "Teach topic to friend"
        ],
        "high": [
            "Complete full revision test",
            "Study for 2 hours deep focus",
            "Write essay or report",
            "Finish full assignment",
            "Attempt mock exam",
            "Prepare presentation slides",
            "Work on project prototype",
            "Summarize entire unit",
            "Create video explainer",
            "Solve complex case study",
            "Research new paper",
            "Practice viva questions",
            "Make question bank",
            "Help peer with doubts",
            "Finish capstone project milestone"
        ]
    },
    "General": {
        "low": [
            "Clean workspace",
            "Organize emails",
            "Make grocery list",
            "Go for 5-minute walk",
            "Water your plants",
            "Declutter desktop files",
            "Do 10-minute meditation",
            "Journal one line of gratitude",
            "Call a friend",
            "Prepare a snack",
            "Stretch lightly",
            "Plan tomorrow’s day",
            "Listen to music",
            "Check bank reminders",
            "Tidy your bed"
        ],
        "medium": [
            "Cook healthy meal",
            "Exercise 20 minutes",
            "Read 5 pages of book",
            "Budget weekly expenses",
            "Organize phone gallery",
            "Respond to pending messages",
            "Plan weekend outing",
            "Clean one room",
            "Write short blog post",
            "Plan errands list",
            "Review personal goals",
            "Pay bills",
            "Read news summary",
            "Learn new word",
            "Sort personal files"
        ],
        "high": [
            "Start new habit tracker",
            "Work on personal project",
            "Finish full workout",
            "Take online course module",
            "Create vision board",
            "Do volunteer work",
            "Complete home organization",
            "Learn new software",
            "Write a journal entry",
            "Start coding challenge",
            "Host study group",
            "Record vlog or reel",
            "Do deep clean",
            "Plan next month budget",
            "Build portfolio site"
        ]
    }
}

# ---------- DETERMINE ENERGY BAND ----------
if energy < 40:
    band = "low"
    st.warning("Low energy — focus on simple, restorative tasks.")
elif energy < 70:
    band = "medium"
    st.info("Moderate energy — balanced tasks are ideal.")
else:
    band = "high"
    st.success("High energy — take on deep-focus work!")

# ---------- DISPLAY TASKS ----------
st.markdown("---")
st.subheader(f"Recommended tasks for a {user_type} ({band.capitalize()} energy)")

for s in suggestions[user_type][band]:
    cols = st.columns([5,1])
    with cols[0]:
        st.write(f"• {s}")
    with cols[1]:
        if st.button("Add", key=f"add_{s}"):
            diff = 1 if band == "low" else (2 if band == "medium" else 3)
            new_task = {
                "id": int(datetime.utcnow().timestamp()),
                "title": s,
                "difficulty": diff,
                "completed": False,
                "created_at": datetime.utcnow().isoformat()
            }
            st.session_state["tasks"].append(new_task)
            st.success(f"Added: {s}")
            st.rerun()

st.markdown("---")
st.caption("🧭 The Browse Agent simulates an intelligent assistant that suggests tasks based on your current mental and physical energy state.")
