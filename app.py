import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from werkzeug.security import check_password_hash
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── CSS THEME ────────────────────────────────────────────────
st.markdown("""
<style>
  /* Background */
  .main { background-color: #F7FAFC; }

  /* Sidebar */
  [data-testid="stSidebar"] { background-color: #0A2342; }
  [data-testid="stSidebar"] * { color: #FFFFFF; font-size: 16px; }

  /* Titles */
  h1, h2, h3, h4 { color: #0A2342; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background-color: #FFFFFF; padding: 15px; border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 5px;
  }

  /* Expanders */
  [data-testid="stExpander"] {
    background-color: #f0f4f8; border: 1px solid #dce3eb;
  }

  /* Buttons */
  .stButton > button {
    background-color: #2CA8D2; color: white; border-radius: 8px;
    padding: 8px 16px;
  }
</style>
""", unsafe_allow_html=True)

# ─── BRAND COLORS ────────────────────────────────────────────
BRAND = ["#2CA8D2", "#21B573", "#0A2342"]

# ─── DATABASE SETUP (placeholder) ───────────────────────────
# Replace with your actual connection string
engine = create_engine("postgresql://user:password@host:5432/flowen_db")

def authenticate(username: str, password: str):
    """Authenticate against users table, return role or None."""
    query = text("SELECT password_hash, role FROM users WHERE username = :u")
    with engine.connect() as conn:
        row = conn.execute(query, {"u": username}).fetchone()
    if row and check_password_hash(row["password_hash"], password):
        return row["role"]
    return None

# ─── SESSION-BASED LOGIN ─────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Flowen Login")
    user = st.text_input("Username")
    pwd  = st.text_input("Password", type="password")
    if st.button("Login"):
        role = authenticate(user, pwd)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("✅ Logged in")
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# ─── LANGUAGE SWITCHER & NAVIGATION ─────────────────────────
lang = st.sidebar.selectbox("🌐 Language", ["🇬🇧 EN", "🇹🇭 TH"])
menu = st.sidebar.radio("", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# ─── LOGO ────────────────────────────────────────────────────
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=160)

# ─── LOAD DATA ───────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")
df = load_data()

# ─── REAL-TIME NOTIFICATIONS ────────────────────────────────
high_risk_count = df[df["dpd"] > 60].shape[0]
if high_risk_count:
    st.warning(f"🔔 {high_risk_count} accounts have exceeded 60 days past due!")

# ─── GLOBAL FILTERS ──────────────────────────────────────────
st.sidebar.markdown("### 🔎 Filters")
regions = st.sidebar.multiselect("Region", options=df["region"].unique(), default=df["region"].unique())
loans   = st.sidebar.multiselect("Loan Type", options=df["loan_type"].unique(), default=df["loan_type"].unique())
min_dpd = st.sidebar.slider("Min Days Past Due", 0, int(df["dpd"].max()), 0)
filtered = df[
    df["region"].isin(regions) &
    df["loan_type"].isin(loans) &
    (df["dpd"] >= min_dpd)
]

# ─── EXPORT FUNCTIONS ────────────────────────────────────────
def to_excel(dataframe):
    return dataframe.to_excel(index=False, engine="openpyxl")

def to_pdf(dataframe):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    style = getSampleStyleSheet()
    elems = [Paragraph("Flowen Debtor Report", style["Title"]), Spacer(1,12)]
    tbl = Table([dataframe.columns.tolist()] + dataframe.values.tolist(), hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,0), colors.HexColor("#2CA8D2")),
        ("TEXTCOLOR", (0,0),(-1,0), colors.white),
        ("GRID", (0,0),(-1,-1), 1, colors.grey),
    ]))
    elems.append(tbl)
    doc.build(elems)
    buf.seek(0)
    return buf

st.sidebar.download_button("⬇️ Excel", data=to_excel(filtered), file_name="flowen_report.xlsx",
                          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.download_button("⬇️ PDF",   data=to_pdf(filtered),   file_name="flowen_report.pdf",
                          mime="application/pdf")

# ─── DEBTOR PROFILE VIEWER ──────────────────────────────────
st.sidebar.markdown("### 👤 Debtor Profile")
selected_name = st.sidebar.selectbox("Select Debtor", filtered["name"].unique())
debtor = df[df["name"] == selected_name].iloc[0]

# ─── PAGE: RISK OVERVIEW ────────────────────────────────────
if menu == "Risk Overview":
    title = "Risk Overview" if lang=="🇬🇧 EN" else "ภาพรวมความเสี่ยง"
    st.title(f"📌 {title}")

    # Metrics
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Accounts Contacted Today", "1,203")
    a2.metric("Responses Received", "645")
    a3.metric("Active Conversations", "53")
    a4.metric("Paid Within 24h", "32%")

    # AI Suggestion
    st.subheader("🔍 AI Suggestion Feed")
    with st.expander("Top 5 likely to pay"):
        st.table(filtered.sort_values("ai_risk_score", ascending=False)
                    .head(5)[["account_id","name","risk_score","loan_type","contact_channel"]]
                    .rename(columns=str.title))

    # Human vs AI
    st.subheader("⚖️ Human vs AI")
    st.dataframe(pd.DataFrame({
      "Method":["AI Flow","Manual Call","Email"],"Success Rate (%)":[72,51,43],"Avg Time (Days)":[2.5,4.2,5.1]
    }))

    # Debtor Profile Expander
    st.subheader("👤 Profile")
    with st.expander(f"{selected_name} — Account {debtor['account_id']}"):
        for k,v in debtor.items():
            st.write(f"**{k.title().replace('_',' ')}:** {v}")

    # Pie: Risk Distribution
    st.subheader("📊 Risk Distribution")
    risk_dist = filtered["risk_level"].value_counts().reset_index()
    risk_dist.columns=["Level","Count"]
    fig = px.pie(risk_dist, names="Level", values="Count", hole=0.4,
                 color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE: JOURNEY MANAGEMENT ───────────────────────────────
elif menu == "Journey Management":
    title = "Journey Management" if lang=="🇬🇧 EN" else "จัดการเส้นทาง"
    st.title(f"🚀 {title}")

    funnel = pd.DataFrame({
      "Stage":["Uncontacted","Contacted","Promise","Paid"],"Count":[8500,5200,2100,865]
    })
    fig = px.funnel(funnel, x="Count", y="Stage", color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Journey Performance")
    st.dataframe(pd.DataFrame({
      "Journey":["LINE A","LINE B","Voice","Manual"],"Conv (%)":[31,42,38,28],"Avg Days":[4.2,3.5,4.0,6.1]
    }))

# ─── PAGE: RECOVERY KPI ─────────────────────────────────────
elif menu == "Recovery KPI":
    title = "Recovery KPI" if lang=="🇬🇧 EN" else "ดัชนีเก็บหนี้"
    st.title(f"💰 {title}")

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total Recovered","฿12.8M")
    m2.metric("Recovery Rate","65%")
    m3.metric("Avg Time","3.6d")
    m4.metric("Collectors","12")

    trend = pd.DataFrame({
      "Date":pd.date_range("2025-07-01",periods=7),"Recovered":[1.0,1.2,1.3,1.1,1.5,1.6,1.7]
    })
    fig = px.line(trend, x="Date", y="Recovered", markers=True,
                  color_discrete_sequence=[BRAND[0]])
    st.plotly_chart(fig, use_container_width=True)

# ─── PAGE: BEHAVIORAL INSIGHTS ──────────────────────────────
elif menu == "Behavioral Insights":
    title = "Behavioral Insights" if lang=="🇬🇧 EN" else "พฤติกรรมลูกหนี้"
    st.title(f"🧠 {title}")

    resp = filtered["response_behavior"].value_counts().reset_index()
    resp.columns=["Behavior","Count"]
    fig = px.pie(resp, names="Behavior", values="Count", hole=0.4,
                 color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

    inc = px.histogram(filtered, x="monthly_income", nbins=30,
                       color_discrete_sequence=[BRAND[1]])
    st.plotly_chart(inc, use_container_width=True)
