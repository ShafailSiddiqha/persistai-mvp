import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Weekly Report", page_icon="📊", layout="wide")

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
}
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



