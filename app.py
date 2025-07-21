import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO
from streamlit_option_menu import option_menu

# ─── Flowen Gradient Color Palette ─────────────────────────────
flowen_colors = ["#00B894", "#00A2C2", "#0984E3"]

# ─── Encode Logo ─────────────────────────────

def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# ─── Page Config ────────────────────────────
st.set_page_config(page_title="Flowen: AI Dashboard", layout="wide")

# ─── Inject Custom CSS ──────────────────────────
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
    body {{
        font-family: 'Inter', sans-serif;
        color: #1C2B36;
        background-color: #F6F8FA;
    }}
    .main .block-container {{
        background-color: #F6F8FA !important;
        padding: 2rem 3rem 3rem 3rem;
    }}
    [data-testid="stSidebar"] {{
        background-color: #0B2A5B;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    .stCard {{
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }}
</style>
<div style='padding: 10px 0 10px 10px;'>
    <img src='data:image/png;base64,{logo_base64}' width='130'/>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar Menu ───────────────────────────
with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=[
            "Risk Overview",
            "Journey Management",
            "Recovery KPI",
            "Behavioral Insights"
        ],
        icons=["bar-chart-line", "bar-chart", "pie-chart", "graph-up"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#0B2A5B"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"color": "#F1F1F1", "font-size": "16px", "--hover-color": "#1C3A6B"},
            "nav-link-selected": {"background-color": "#29C2D1", "color": "#0B2A5B", "font-weight": "bold"},
        }
    )

# ─── Navigation Handler ─────────────────────────
if selected == "Risk Overview":
    st.switch_page("pages/1_\ud83d\udcca_Risk_Overview.py")
elif selected == "Journey Management":
    st.switch_page("pages/2_\ud83e\uddeb_Journey_Management.py")
elif selected == "Recovery KPI":
    st.switch_page("pages/3_\ud83d\udcca_Recovery_KPI.py")
elif selected == "Behavioral Insights":
    st.switch_page("pages/4_\ud83d\udd1d_Behavioral_Insights.py")
