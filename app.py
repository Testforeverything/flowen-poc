import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# ─── TRY IMPORT SQLALCHEMY ─────────────────────────────────────
try:
    from sqlalchemy import create_engine, text
    from werkzeug.security import check_password_hash
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# ─── PAGE CONFIG & THEME ───────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")
st.markdown("""
<style>
  .main { background-color: #F7FAFC; }
  [data-testid="stSidebar"] { background-color: #0A2342; }
  [data-testid="stSidebar"] * { color: #FFFFFF; font-size: 16px; }
  h1,h2,h3,h4 { color: #0A2342; }
  div[data-testid="metric-container"] {
    background-color: #FFFFFF; padding:15px; border-radius:12px;
    box-shadow:0 1px 3px rgba(0,0,0,0.1); margin:5px;
  }
  .stButton > button {
    background-color: #2CA8D2; color:white; border-radius:8px; padding:8px 16px;
  }
  [data-testid="stExpander"] {
    background-color:#f0f4f8; border:1px solid #dce3eb;
  }
</style>
""", unsafe_allow_html=True)

# ─── BRAND COLORS ─────────────────────────────────────────────
BRAND = ["#2CA8D2", "#21B573", "#0A2342"]

# ─── DATABASE SETUP IF AVAILABLE ──────────────────────────────
if DB_AVAILABLE:
    engine = create_engine("postgresql://user:password@host:5432/flowen_db")

def authenticate(username: str, password: str):
    """Authenticate user: DB if available, else fallback."""
    if DB_AVAILABLE:
        q = text("SELECT password_hash, role FROM users WHERE username=:u")
        with engine.connect() as conn:
            row = conn.execute(q, {"u": username}).fetchone()
        if row and check_password_hash(row["password_hash"], password):
            return row["role"]
        return None
    else:
        # Fallback local users
        FALLBACK = {
            "admin": {"pwd": "1234", "role": "admin"},
            "user":  {"pwd": "pass", "role": "viewer"}
        }
        user = FALLBACK.get(username)
        if user and password == user["pwd"]:
            return user["role"]
        return None

# ─── SESSION-BASED LOGIN ───────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Flowen Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        role = authenticate(u, p)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("✅ Logged in")
            if not DB_AVAILABLE:
                st.warning("⚠️ Using fallback login — please install sqlalchemy for production.")
        else:
            st.error("❌ Invalid credentials")
    st.stop()

# ─── LOAD DATA ────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")
df = load_data()

# ─── LANGUAGE & NAVIGATION ───────────────────────────────────
lang = st.sidebar.selectbox("🌐 Language", ["🇬🇧 EN", "🇹🇭 TH"])
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=160)
menu = st.sidebar.radio("", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# ─── REAL-TIME ALERT ──────────────────────────────────────────
high = df[df["dpd"] > 60].shape[0]
if high:
    st.warning(f"🔔 {high} accounts exceeded 60 days past due!")

# ─── GLOBAL FILTERS ──────────────────────────────────────────
st.sidebar.markdown("### 🔎 Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), df["region"].unique())
loans   = st.sidebar.multiselect("Loan Type", df["loan_type"].unique(), df["loan_type"].unique())
min_dpd = st.sidebar.slider("Min Days Past Due", 0, int(df["dpd"].max()), 0)
filtered = df[df["region"].isin(regions) & df["loan_type"].isin(loans) & (df["dpd"] >= min_dpd)]

# ─── EXPORT BUTTONS ──────────────────────────────────────────
def to_excel(d):
    return d.to_excel(index=False, engine="openpyxl")
def to_pdf(d):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    style = getSampleStyleSheet()
    elems = [Paragraph("Flowen Debtor Report", style["Title"]), Spacer(1,12)]
    data = [d.columns.tolist()] + d.values.tolist()
    tbl = Table(data, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor(BRAND[0])),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
    ]))
    elems.append(tbl)
    doc.build(elems)
    buf.seek(0)
    return buf

st.sidebar.download_button("⬇️ Excel", data=to_excel(filtered),
    file_name="flowen_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.download_button("⬇️ PDF", data=to_pdf(filtered),
    file_name="flowen_report.pdf", mime="application/pdf")

# ─── DEBTOR PROFILE VIEW ──────────────────────────────────────
st.sidebar.markdown("### 👤 Debtor Profile")
sel = st.sidebar.selectbox("Select", filtered["name"].unique())
deb = df[df["name"]==sel].iloc[0]

# ─── PAGES ────────────────────────────────────────────────────
if menu=="Risk Overview":
    t = "Risk Overview" if lang=="🇬🇧 EN" else "ภาพรวมความเสี่ยง"
    st.title(f"📌 {t}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Contacted", "1,203"); c2.metric("Responses","645")
    c3.metric("Active Conv.","53");  c4.metric("Paid 24h","32%")
    st.subheader("🔍 AI Suggestions")
    with st.expander("Top 5"):
        st.table(filtered.nlargest(5,"ai_risk_score")
            [["account_id","name","risk_score","loan_type","contact_channel"]]
            .rename(columns=str.title))
    st.subheader("👤 Profile")
    with st.expander(f"{sel} ({deb['account_id']})"):
        for k,v in deb.items():
            st.write(f"**{k.title()}:** {v}")
    st.subheader("📊 Risk Dist.")
    rd = filtered["risk_level"].value_counts().reset_index()
    rd.columns=["Level","Count"]
    fig = px.pie(rd, names="Level", values="Count", hole=0.4,
                 color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

elif menu=="Journey Management":
    t = "Journey Management" if lang=="🇬🇧 EN" else "จัดการการเดินทาง"
    st.title(f"🚀 {t}")
    funnel=pd.DataFrame({"Stage":["U","C","P","Paid"],"Count":[8500,5200,2100,865]})
    fig=px.funnel(funnel,x="Count",y="Stage",color_discrete_sequence=BRAND)
    st.plotly_chart(fig,use_container_width=True)
    st.subheader("📈 Perf")
    st.dataframe(pd.DataFrame({
      "Journey":["A","B","C","D"],"Conv%":[31,42,38,28],"Days":[4.2,3.5,4.0,6.1]
    }))

elif menu=="Recovery KPI":
    t = "Recovery KPI" if lang=="🇬🇧 EN" else "ดัชนีเก็บหนี้"
    st.title(f"💰 {t}")
    m1,m2,m3,m4=st.columns(4)
    m1.metric("Recovered","฿12.8M"); m2.metric("Rate","65%")
    m3.metric("Time","3.6d");      m4.metric("Cols","12")
    trend=pd.DataFrame({"Date":pd.date_range("2025-07-01",7),
                        "Rec":[1.0,1.2,1.3,1.1,1.5,1.6,1.7]})
    fig=px.line(trend,x="Date",y="Rec",markers=True,
                color_discrete_sequence=[BRAND[0]])
    st.plotly_chart(fig,use_container_width=True)

else:  # Behavioral Insights
    t = "Behavioral Insights" if lang=="🇬🇧 EN" else "พฤติกรรมลูกหนี้"
    st.title(f"🧠 {t}")
    br = filtered["response_behavior"].value_counts().reset_index()
    br.columns=["B","C"]
    fig=px.pie(br,names="B",values="C",hole=0.4,
               color_discrete_sequence=BRAND)
    st.plotly_chart(fig,use_container_width=True)
    fig2=px.histogram(filtered,x="monthly_income",nbins=30,
                      color_discrete_sequence=[BRAND[1]])
    st.plotly_chart(fig2,use_container_width=True)
