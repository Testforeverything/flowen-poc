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

# ─── CUSTOM THEME CSS ───────────────────────────────────────
st.markdown("""
<style>
  /* Main background */
  .main { background-color: #F7FAFC; }
  /* Sidebar */
  [data-testid="stSidebar"] { background-color: #0A2342; }
  [data-testid="stSidebar"] * { color: #FFFFFF; font-size: 16px; }
  /* Titles */
  h1,h2,h3,h4 { color: #0A2342; }
  /* Metric cards */
  div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 5px;
  }
  /* Expanders */
  [data-testid="stExpander"] {
    background-color: #f0f4f8;
    border: 1px solid #dce3eb;
  }
  /* Buttons */
  .stButton > button {
    background-color: #2CA8D2;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
  }
</style>
""", unsafe_allow_html=True)

# ─── BRAND COLORS ───────────────────────────────────────────
BRAND = ["#2CA8D2", "#21B573", "#0A2342"]

# ─── LOAD DATA ───────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── SIDEBAR: LOGO, LANGUAGE, MENU, FILTERS, EXPORT ─────────
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=150)

lang = st.sidebar.selectbox("🌐 Language", ["🇬🇧 EN", "🇹🇭 TH"])

menu = st.sidebar.radio("📊 Navigation", [
    "Risk Overview",
    "Journey Management",
    "Recovery KPI",
    "Behavioral Insights"
])

st.sidebar.markdown("### 🔎 Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), df["region"].unique())
loans   = st.sidebar.multiselect("Loan Type", df["loan_type"].unique(), df["loan_type"].unique())
min_dpd = st.sidebar.slider("Min Days Past Due", 0, int(df["dpd"].max()), 0)

filtered = df[
    df["region"].isin(regions) &
    df["loan_type"].isin(loans) &
    (df["dpd"] >= min_dpd)
]

# Export Excel
def to_excel(data):
    buf = BytesIO()
    data.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()

# Export PDF
def to_pdf(data):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elems = [Paragraph("Flowen Debtor Report", styles["Title"]), Spacer(1,12)]
    table_data = [data.columns.tolist()] + data.values.tolist()
    tbl = Table(table_data, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor(BRAND[0])),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
    ]))
    elems.append(tbl)
    doc.build(elems)
    return buf.getvalue()

st.sidebar.download_button("⬇️ Export Excel", to_excel(filtered),
    file_name="flowen_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.download_button("⬇️ Export PDF", to_pdf(filtered),
    file_name="flowen_report.pdf",
    mime="application/pdf")

# ─── REAL-TIME ALERT ────────────────────────────────────────
overdue = df[df["dpd"] > 60].shape[0]
if overdue:
    st.warning(f"🔔 {overdue} accounts have exceeded 60 days past due!")

# ─── DEBTOR PROFILE VIEWER ──────────────────────────────────
st.sidebar.markdown("### 👤 Debtor Profile")
sel_name = st.sidebar.selectbox("Select Debtor", filtered["name"].unique())
debtor = df[df["name"] == sel_name].iloc[0]

# ─── PAGES ───────────────────────────────────────────────────
if menu == "Risk Overview":
    title = "Risk Overview" if lang=="🇬🇧 EN" else "ภาพรวมความเสี่ยง"
    st.title(f"📌 {title}")

    # Real-Time Status
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Accounts Contacted Today", "1,203")
    c2.metric("Responses Received", "645")
    c3.metric("Active Conversations", "53")
    c4.metric("Paid Within 24h", "32%")

    # AI Suggestion Feed
    st.markdown("### 🔍 AI Suggestion Feed")
    with st.expander("Top 5 Accounts Likely to Pay in 48h"):
        top5 = filtered.nlargest(5, "ai_risk_score")
        st.table(top5[["account_id","name","risk_score","loan_type","contact_channel"]]
                 .rename(columns=str.title))

    with st.expander("Accounts Ignored All Contact for 7+ Days"):
        stale = filtered[filtered["last_payment_days_ago"] > 30].nlargest(5, "risk_score")
        st.dataframe(stale[["account_id","name","risk_score","last_payment_days_ago","region"]]
                     .rename(columns={
                         "account_id":"Account ID","name":"Name",
                         "risk_score":"Risk Score",
                         "last_payment_days_ago":"Days Ago","region":"Region"
                     }), use_container_width=True)

    # Human vs AI
    st.markdown("### ⚖️ Human vs AI Effectiveness")
    st.dataframe(pd.DataFrame({
        "Method":["AI Recommended Flow","Manual Call","Email Follow-up"],
        "Success Rate (%)":[72,51,43],
        "Avg Time to Payment (Days)":[2.5,4.2,5.1]
    }))

    # Debtor Profile
    st.markdown("### 👤 Debtor Profile")
    with st.expander(f"{sel_name} ({debtor['account_id']})"):
        for k,v in debtor.items():
            st.write(f"**{k.replace('_',' ').title()}:** {v}")

    # Risk Distribution
    st.markdown("### 📊 Risk Distribution")
    rd = filtered["risk_level"].value_counts().reset_index()
    rd.columns = ["Level","Count"]
    fig = px.pie(rd, names="Level", values="Count", hole=0.4,
                 color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Journey Management":
    title = "Journey Management" if lang=="🇬🇧 EN" else "จัดการเส้นทาง"
    st.title(f"🚀 {title}")

    st.markdown("### 📊 Journey Funnel Overview")
    funnel = pd.DataFrame({
        "Stage":["Uncontacted","Contacted","Promise to Pay","Paid"],
        "Count":[8500,5200,2100,865]
    })
    fig = px.funnel(funnel, x="Count", y="Stage",
                    color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📈 Journey Type Performance")
    st.dataframe(pd.DataFrame({
        "Journey":["LINE A","LINE B","Voice Prompt","Manual Call"],
        "Conversion Rate (%)":[31,42,38,28],
        "Avg Days to Pay":[4.2,3.5,4.0,6.1]
    }))

elif menu == "Recovery KPI":
    title = "Recovery KPI" if lang=="🇬🇧 EN" else "ดัชนีการเก็บหนี้"
    st.title(f"💰 {title}")

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Total Recovered","฿12,850,000")
    col2.metric("Recovery Rate","65%")
    col3.metric("Avg Time to Recovery","3.6 days")
    col4.metric("Active Collectors","12")

    st.markdown("### 📈 Daily Recovery Trend")
    trend = pd.DataFrame({
        "Date":pd.date_range("2025-07-01", periods=10, freq="D"),
        "Recovered":[1e6,1.25e6,1.38e6,1.22e6,1.5e6,1.6e6,1.7e6,1.45e6,1.55e6,1.65e6]
    })
    fig = px.line(trend, x="Date", y="Recovered", markers=True,
                  color_discrete_sequence=[BRAND[0]])
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Behavioral Insights":
    title = "Behavioral Insights" if lang=="🇬🇧 EN" else "พฤติกรรมลูกหนี้"
    st.title(f"🧠 {title}")

    st.markdown("### 🎯 Response Behavior")
    rb = filtered["response_behavior"].value_counts().reset_index()
    rb.columns=["Behavior","Count"]
    fig = px.pie(rb, names="Behavior", values="Count", hole=0.4,
                 color_discrete_sequence=BRAND)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💸 Monthly Income Distribution")
    fig2 = px.histogram(filtered, x="monthly_income", nbins=30,
                        color_discrete_sequence=[BRAND[1]])
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📡 Channel vs Behavior")
    cb = filtered.groupby(["contact_channel","response_behavior"])\
                 .size().reset_index(name="Count")
    fig3 = px.bar(cb, x="contact_channel", y="Count",
                  color="response_behavior", barmode="group",
                  color_discrete_sequence=BRAND)
    st.plotly_chart(fig3, use_container_width=True)
