import streamlit as st
import base64
from PIL import Image
from io import BytesIO

# ─── Load & Encode Logo ─────────────────────────────────────────
def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# ─── Inject Logo + Language Toggle + Theme ──────────────────────
st.markdown(f"""
    <style>
    /* --- Card Styling --- */
    div[data-testid="stExpander"], .stContainer {{
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}
    /* --- Metric Cards --- */
    [data-testid="metric-container"] {{
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        text-align: center;
    }}
    /* --- Sidebar --- */
    [data-testid="stSidebar"] {{
        background-color: #0a2342;
    }}
    [data-testid="stSidebar"] .css-1v3fvcr {{
        color: white;
    }}
    /* --- Language Toggle --- */
    .lang-toggle {{
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 1000;
    }}
    </style>

    <!-- Logo Top-Left -->
    <div style="position:fixed; top:10px; left:10px; z-index:1000;">
        <img src="data:image/png;base64,{logo_base64}" width="140"/>
    </div>

    <!-- Language Toggle Top-Right -->
    <div class="lang-toggle">
        <select onchange="window.location.href='?lang='+this.value">
            <option value="en" selected>🇬🇧 EN</option>
            <option value="th">🇹🇭 TH</option>
        </select>
    </div>
""", unsafe_allow_html=True)
