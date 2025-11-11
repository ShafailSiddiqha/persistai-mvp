import streamlit as st
import random

st.set_page_config(page_title="Weekly Report", page_icon="📊", layout="wide")

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
.metric-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(120,120,160,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------- STATS ----------
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "xp" not in st.session_state:
    st.session_state["xp"] = 0

tasks = st.session_state["tasks"]
total = len(tasks)
done = len([t for t in tasks if t.get("completed")])
xp = st.session_state["xp"]
completion = (done / total * 100) if total else 0
avg_energy = random.randint(60, 95)

# ---------- UI ----------
st.title("📊 Weekly Report")
st.caption("A snapshot of your week’s progress and focus trends.")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><h3>{done}</h3><p>Tasks Completed</p></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><h3>{xp}</h3><p>Total XP</p></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><h3>{completion:.1f}%</h3><p>Completion Rate</p></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><h3>{avg_energy}%</h3><p>Avg Energy</p></div>', unsafe_allow_html=True)

st.markdown("---")

if completion == 0:
    st.info("No tasks yet! Add some in the Tasks Manager.")
elif completion < 50:
    st.warning("⚠️ Productivity dipped this week. Try smaller tasks tomorrow.")
elif xp < 100:
    st.info("💡 Momentum building — medium tasks will help grow XP faster.")
else:
    st.success("🎉 Great week! Your ADHD flow is improving steadily.")
