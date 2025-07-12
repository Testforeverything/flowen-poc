
import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import plotly.express as px

# ─── Set up Flowen CI Color Palette ──────────────────────────────
flowen_colors = ["#00B894", "#0984E3", "#FDCB6E", "#6C5CE7", "#00CEC9"]

# ─── Logo Encoding ───────────────────────────────────────────────
def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ─── Inject UI Theme: Logo + Language + CSS ──────────────────────
def inject_ui_theme(logo_path="flowen_logo.png"):
    logo_base64 = get_base64_logo(logo_path)
    st.markdown(f"""
        <style>
        div[data-testid="stExpander"], .stContainer {{
            border-radius: 15px;
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        [data-testid="metric-container"] {{
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            text-align: center;
        }}
        [data-testid="stSidebar"] {{
            background-color: #0a2342;
        }}
        [data-testid="stSidebar"] .css-1v3fvcr {{
            color: white;
        }}
        .lang-toggle {{
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 1000;
        }}
        </style>

        <div style="position:fixed; top:10px; left:10px; z-index:1000;">
            <img src="data:image/png;base64,{logo_base64}" width="140"/>
        </div>

        <div class="lang-toggle">
            <select onchange="window.location.href='?lang='+this.value">
                <option value="en" selected>🇬🇧 EN</option>
                <option value="th">🇹🇭 TH</option>
            </select>
        </div>
    """, unsafe_allow_html=True)

# ─── Flowen Chart Wrappers ───────────────────────────────────────
def flowen_pie(data, names, values, title=""):
    return px.pie(
        data,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=flowen_colors,
        hole=0.4
    )

def flowen_bar(data, x, y, color=None, title="", barmode=None):
    return px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=flowen_colors,
        barmode=barmode
    )

def flowen_line(data, x, y, title=""):
    return px.line(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=flowen_colors,
        markers=True
    )

def flowen_funnel(data, x, y, title=""):
    return px.funnel(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=flowen_colors
    )

def flowen_histogram(data, x, nbins=30, title=""):
    return px.histogram(
        data,
        x=x,
        nbins=nbins,
        title=title,
        color_discrete_sequence=flowen_colors
    )
