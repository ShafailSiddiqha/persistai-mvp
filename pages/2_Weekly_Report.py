import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Weekly Report", page_icon="📊", layout="wide")

# ---------- THEME ----------
st.markdown("""
<style>
/* 🌈 Unified Theme for PersistAI */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAF8FF 0%, #FDFBFF 100%);
    color: #2B2B2B;
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
    border-right: 1px solid #E2E8F0;
}
h1, h2, h3 { color: #5A3EBA; font-weight: 700; }

.metric-card {
    background: white;
    border-radius: 12px;
    text-align: center;
    padding: 1rem;
    box-shadow: 0 4px 10px rgba(120,120,160,0.1);
    font-size: 1rem;
}
.completed-box {
    background: #E8F5E9;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.pending-box {
    background: #FFF9C4;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Progress fade-in */
.stPlotlyChart, .stMarkdown {
    animation: fadein 1.2s ease-in;
}
@keyframes fadein {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* ---------- MOBILE RESPONSIVE ---------- */
@media only screen and (max-width: 768px) {
    [data-testid="stAppViewContainer"] { padding: 0.8rem !important; }
    h1, h2, h3 { text-align: center !important; font-size: 1.25rem !important; }
    .metric-card { font-size: 0.9rem !important; padding: 0.8rem !important; margin-bottom: 8px !important; }
    .completed-box, .pending-box { font-size: 0.9rem !important; }
    footer { text-align: center !important; font-size: 0.8rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "tasks" not in st.session_state: st.session_state["tasks"] = []
if "xp" not in st.session_state: st.session_state["xp"] = 0

# ---------- DATA ----------
tasks = st.session_state["tasks"]
done = [t for t in tasks if t.get("completed")]
pending = [t for t in tasks if not t.get("completed")]
xp = st.session_state["xp"]
completion_rate = (len(done) / len(tasks) * 100) if tasks else 0
avg_energy = random.randint(60, 95)

# ---------- HEADER ----------
st.title("📊 Weekly Report")
st.caption("Track your ADHD flow performance for this week.")

# ---------- METRIC CARDS ----------
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='metric-card'><h3>{len(done)}</h3><p>Completed</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><h3>{len(pending)}</h3><p>Pending</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><h3>{xp}</h3><p>Total XP</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><h3>{completion_rate:.1f}%</h3><p>Completion Rate</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- DONUT CHART ----------
if tasks:
    st.subheader("📈 Task Distribution")
    labels = ['Completed', 'Pending']
    sizes = [len(done), len(pending)]
    colors = ['#81C784', '#FBC02D']

    fig, ax = plt.subplots(figsize=(3, 3))  # smaller donut size
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'width': 0.4, 'edgecolor': 'white'},
        textprops={'fontsize': 9, 'color': '#333'}
    )

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')
    st.pyplot(fig, use_container_width=False)

st.markdown("---")

# ---------- TASK DETAILS ----------
st.subheader("✅ Completed Tasks")
if done:
    for t in done:
        st.markdown(f"<div class='completed-box'><b>{t['title']}</b><br><small>Completed ✔️</small></div>", unsafe_allow_html=True)
else:
    st.info("No tasks completed yet.")

st.subheader("⏳ Pending Tasks")
if pending:
    for t in pending:
        st.markdown(f"<div class='pending-box'><b>{t['title']}</b><br><small>Pending — Difficulty {t['difficulty']}</small></div>", unsafe_allow_html=True)
else:
    st.success("🎯 All tasks completed — nothing pending!")

st.markdown("<center><small>Built by <b>Shafail Siddiqha</b> — Weekly Flow Analytics</small></center>", unsafe_allow_html=True)
