import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Weekly Report", page_icon="📊", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FDFBFF 0%, #FAF7FF 100%);
    font-family: 'Poppins', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E3DFFD 0%, #DFF5FF 100%);
}
.metric-card {
    background-color: #fff;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 3px 12px rgba(120,120,160,0.1);
}
.pending-box {border-left: 6px solid #FBC02D; background:#fff;padding:10px;border-radius:8px;}
.completed-box {border-left: 6px solid #81C784;background:#fff;padding:10px;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

if "tasks" not in st.session_state: st.session_state["tasks"] = []
if "xp" not in st.session_state: st.session_state["xp"] = 0

tasks = st.session_state["tasks"]
done = [t for t in tasks if t.get("completed")]
pending = [t for t in tasks if not t.get("completed")]
xp = st.session_state["xp"]
completion_rate = (len(done) / len(tasks) * 100) if tasks else 0
avg_energy = random.randint(60, 95)

st.title("📊 Weekly Report")
st.caption("See your ADHD flow progress this week!")

# Stats cards
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='metric-card'><h3>{len(done)}</h3><p>Completed</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><h3>{len(pending)}</h3><p>Pending</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><h3>{xp}</h3><p>Total XP</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><h3>{completion_rate:.1f}%</h3><p>Completion Rate</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- DONUT PIE CHART ----------
if tasks:
    st.subheader("📈 Task Distribution")

    labels = ['Completed', 'Pending']
    sizes = [len(done), len(pending)]
    colors = ['#81C784', '#FBC02D']

    # Donut chart (smaller, centered)
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'width': 0.4, 'edgecolor': 'white'},  # donut style
        textprops={'fontsize': 10, 'color': '#333'}
    )

    # Center circle (white inner space)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')

    # Add subtle animation / fade-in
    st.markdown(
        """
        <style>
        .stPlotlyChart, .stMarkdown {
            animation: fadein 1.2s ease-in;
        }
        @keyframes fadein {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.pyplot(fig, use_container_width=False)


# Task details
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

