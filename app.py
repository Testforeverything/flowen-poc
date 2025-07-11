import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# ─── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── CUSTOM CSS THEME ───────────────────────────────────────
st.markdown("""
<style>
  /* Global background */
  .main { background-color: #F7FAFC; }

  /* Top bar */
  .top-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
  .top-bar img { height: 40px; }
  .top-bar .lang { font-size: 1rem; }

  /* Sidebar background */
  [data-testid="stSidebar"] { background-color: #0A2342; }
  [data-testid="stSidebar"] * { color: #FFF; }

  /* Card style */
  .card { background: #FFF; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1); }

  /* Headings */
  h2, h3, .card h4 { color: #0A2342; }

  /* Buttons */
  .stButton>button { background-color: #2CA8D2; color: #FFF; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─── BRAND COLORS ───────────────────────────────────────────
BRAND = ["#2CA8D2", "#21B573", "#0A2342"]

# ─── LOAD DATA ───────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── TOP BAR: LOGO + TITLE + LANGUAGE SWITCH ───────────────
col1, col2, col3 = st.columns([1, 8, 1])
with col1:
    st.image("https://i.imgur.com/UOa1y7O.png")
with col2:
    title = "Debt Collection AI" if True else ""  # placeholder
    st.markdown(f"<h1 style='color:#0A2342'>Flowen: {title}</h1>", unsafe_allow_html=True)
with col3:
    lang = st.selectbox("", ["🇬🇧 EN", "🇹🇭 TH"], key="lang", label_visibility="collapsed")

st.markdown("---", unsafe_allow_html=True)

# ─── SIDEBAR MENU & FILTERS & EXPORT ───────────────────────
st.sidebar.header("📊 Navigation")
menu = st.sidebar.radio("", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

st.sidebar.markdown("### 🔎 Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), df["region"].unique())
loans   = st.sidebar.multiselect("Loan Type", df["loan_type"].unique(), df["loan_type"].unique())
min_dpd = st.sidebar.slider("Min Days Past Due", 0, int(df["dpd"].max()), 0)

filtered = df[
    df["region"].isin(regions) &
    df["loan_type"].isin(loans) &
    (df["dpd"] >= min_dpd)
]

def to_excel(data):
    buf = BytesIO()
    data.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()

def to_pdf(data):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elems = [Paragraph("Flowen Debtor Report", styles["Title"]), Spacer(1,12)]
    table_data = [data.columns.tolist()] + data.values.tolist()
    tbl = Table(table_data, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor(BRAND[0])),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
    ]))
    elems.append(tbl)
    doc.build(elems)
    return buf.getvalue()

st.sidebar.download_button("⬇️ Export Excel", to_excel(filtered),
    file_name="flowen_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.download_button("⬇️ Export PDF", to_pdf(filtered),
    file_name="flowen_report.pdf", mime="application/pdf")

# ─── REAL-TIME ALERT ────────────────────────────────────────
late = df[df["dpd"] > 60].shape[0]
if late:
    st.warning(f"🔔 {late} accounts have exceeded 60 days past due!")

# ─── DEBTOR PROFILE VIEWER ──────────────────────────────────
st.sidebar.markdown("### 👤 Debtor Profile")
sel = st.sidebar.selectbox("Select Debtor", filtered["name"].unique())
debtor = df[df["name"] == sel].iloc[0]

# ─── PAGE: RISK OVERVIEW ────────────────────────────────────
if menu == "Risk Overview":
    header = "Risk Overview" if lang=="🇬🇧 EN" else "ภาพรวมความเสี่ยง"
    st.markdown(f"<h2>{header}</h2>", unsafe_allow_html=True)

    # Real-time status panel
    with st.container():
        st.markdown('<div class="card"><h4>Real-Time Status</h4>' +
                    '<div style="display:flex;gap:1rem">' +
                    '<div>📞 <b>1,203</b><br>Contacted Today</div>' +
                    '<div>✉️ <b>645</b><br>Responses</div>' +
                    '<div>💬 <b>53</b><br>Active Conv.</div>' +
                    '<div>💰 <b>32%</b><br>Paid 24h</div>' +
                    '</div></div>', unsafe_allow_html=True)

    # AI Suggestion Feed
    with st.container():
        st.markdown('<div class="card"><h4>AI Suggestion Feed</h4></div>', unsafe_allow_html=True)
        with st.expander("Top 5 Accounts Likely to Pay in 48h"):
            st.table(filtered.nlargest(5,"ai_risk_score")[["account_id","name","risk_score","loan_type","contact_channel"]]
                     .rename(columns=str.title))

    # Human vs AI
    with st.container():
        st.markdown('<div class="card"><h4>⚖️ Human vs AI Effectiveness</h4></div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({
            "Method":["AI Flow","Manual Call","Email"],
            "Success Rate (%)":[72,51,43],
            "Avg Time to Pay":[2.5,4.2,5.1]
        }))

    # Debtor Profile
    with st.container():
        st.markdown('<div class="card"><h4>👤 Debtor Profile</h4></div>', unsafe_allow_html=True)
        with st.expander(f"{sel} ({debtor['account_id']})"):
            for k,v in debtor.items():
                st.write(f"**{k.replace('_',' ').title()}:** {v}")

    # Risk Distribution Pie
    with st.container():
        st.markdown('<div class="card"><h4>📊 Risk Distribution</h4></div>', unsafe_allow_html=True)
        rd = filtered["risk_level"].value_counts().reset_index()
        rd.columns = ["Level","Count"]
        fig = px.pie(rd, names="Level", values="Count", hole=0.4,
                     color_discrete_sequence=BRAND)
        st.plotly_chart(fig, use_container_width=True)

# ─── PAGE: JOURNEY MANAGEMENT ───────────────────────────────
elif menu == "Journey Management":
    header = "Journey Management" if lang=="🇬🇧 EN" else "จัดการการเดินทาง"
    st.markdown(f"<h2>{header}</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><h4>📊 Journey Funnel Overview</h4></div>', unsafe_allow_html=True)
        funnel = pd.DataFrame({
            "Stage":["Uncontacted","Contacted","Promise to Pay","Paid"],
            "Count":[8500,5200,2100,865]
        })
        fig = px.funnel(funnel, x="Count", y="Stage", color_discrete_sequence=BRAND)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('<div class="card"><h4>📈 Journey Type Performance</h4></div>', unsafe_allow_html=True)
        st.table(pd.DataFrame({
            "Journey":["LINE A","LINE B","Voice","Manual"],
            "Conv Rate (%)":[31,42,38,28],
            "Avg Days":[4.2,3.5,4.0,6.1]
        }))

# ─── PAGE: RECOVERY KPI ─────────────────────────────────────
elif menu == "Recovery KPI":
    header = "Recovery KPI" if lang=="🇬🇧 EN" else "ดัชนีการเก็บหนี้"
    st.markdown(f"<h2>{header}</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><h4>💰 KPI Summary</h4></div>', unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Total Recovered","฿12.85M")
        m2.metric("Recovery Rate","65%")
        m3.metric("Avg Time to Recovery","3.6d")
        m4.metric("Collectors","12")

    with st.container():
        st.markdown('<div class="card"><h4>📈 Daily Recovery Trend</h4></div>', unsafe_allow_html=True)
        trend = pd.DataFrame({
            "Date":pd.date_range("2025-07-01",periods=7),
            "Recovered":[1.0,1.2,1.3,1.1,1.5,1.6,1.7]
        })
        fig = px.line(trend, x="Date", y="Recovered", markers=True,
                      color_discrete_sequence=[BRAND[0]])
        st.plotly_chart(fig, use_container_width=True)

# ─── PAGE: BEHAVIORAL INSIGHTS ──────────────────────────────
else:
    header = "Behavioral Insights" if lang=="🇬🇧 EN" else "พฤติกรรมลูกหนี้"
    st.markdown(f"<h2>{header}</h2>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card"><h4>🎯 Response Behavior</h4></div>', unsafe_allow_html=True)
        rb = filtered["response_behavior"].value_counts().reset_index()
        rb.columns=["Behavior","Count"]
        fig = px.pie(rb, names="Behavior", values="Count", hole=0.4,
                     color_discrete_sequence=BRAND)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('<div class="card"><h4>💸 Monthly Income Distribution</h4></div>', unsafe_allow_html=True)
        fig2 = px.histogram(filtered, x="monthly_income", nbins=30,
                            color_discrete_sequence=[BRAND[1]])
        st.plotly_chart(fig2, use_container_width=True)

    with st.container():
        st.markdown('<div class="card"><h4>📡 Channel vs Behavior</h4></div>', unsafe_allow_html=True)
        cb = filtered.groupby(["contact_channel","response_behavior"])\
                     .size().reset_index(name="Count")
        fig3 = px.bar(cb, x="contact_channel", y="Count",
                      color="response_behavior", barmode="group",
                      color_discrete_sequence=BRAND)
        st.plotly_chart(fig3, use_container_width=True)
