# flowen_dashboard_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── Load Flowen Logo from base64 ─────────────────────────────────────────────
logo_base64 = """<Flowen_logo>"""

st.markdown(
    f'''
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" width="140" style="margin-bottom:10px;" />
        <select onchange="window.location.search='lang='+this.value" style="padding:5px;border-radius:5px;">
            <option value="en">\ud83c\uddec\ud83c\udee7 EN</option>
            <option value="th">\ud83c\uddf9\ud83c\udded TH</option>
        </select>
    </div>
    <hr style="margin-top:10px; margin-bottom:20px;">
    ''',
    unsafe_allow_html=True
)

# ─── Global Style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="column"] > div {
    border: 1px solid #E0E0E0;
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    background-color: #ffffff;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─── Realtime Notification Mock ───────────────────────────────────────────────
st.markdown("""
<div style="background-color:#e8f9f0;border-left:6px solid #0aaf8d;padding:10px 20px;margin-bottom:20px;">
  \ud83d\udd14 <strong>Realtime Alert:</strong> 3 accounts exceeded 45+ DPD today. <a href="#">[View Now]</a>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── Color Theme ──────────────────────────────────────────────────────────────
FLOWEN_COLORS = ["#0aaf8d", "#28c7fa", "#005f73"]

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
menu = st.sidebar.radio("Navigation", [
    "Risk Overview",
    "Journey Management",
    "Recovery KPI",
    "Behavioral Insights"
])
