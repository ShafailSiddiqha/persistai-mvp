# pages/2_Weekly_Report.py — Weekly Report page
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

import json, os, random

st.set_page_config(page_title="Weekly Report", page_icon="📊", layout="wide")

DATA_FILE = "data.json"
def load_data():
    if not os.path.exists(DATA_FILE):
        default = {"tasks": [], "xp": 0}
        with open(DATA_FILE, "w") as f: json.dump(default, f)
        return default
    with open(DATA_FILE, "r") as f: return json.load(f)

data = load_data()

total = len(data["tasks"])
done = len([t for t in data["tasks"] if t.get("done")])
xp = data.get("xp", 0)
completion_rate = (done / total * 100) if total else 0
avg_energy = random.randint(60, 95)

st.title("📊 Weekly Summary")
st.caption("Auto-generated insights from your task activity")

st.markdown("""
<style>
.report-box {background: linear-gradient(135deg,#f5f0ff,#ffffff); padding:1.5rem; border-radius:14px; box-shadow:0 6px 18px rgba(120,120,180,0.06);}
.metric-card {background-color:#fff; padding:1rem; border-radius:10px; text-align:center; box-shadow:0 2px 10px rgba(80,80,120,0.06);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="report-box">', unsafe_allow_html=True)
st.subheader("This Week’s Highlights")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><h3>{done}</h3><p>Tasks Completed</p></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><h3>{xp}</h3><p>Total XP</p></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><h3>{completion_rate:.1f}%</h3><p>Completion Rate</p></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><h3>{avg_energy}%</h3><p>Avg Energy</p></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")
if completion_rate < 50:
    st.warning("⚠️ Productivity dipped this week. Consider scheduling lighter tasks or recovery time.")
elif xp < 100:
    st.info("💡 Momentum-building — keep completing medium tasks for quick XP.")
else:
    st.success("🎉 Great week! Your XP and completion rate are strong.")
