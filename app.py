
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# ---- PAGE CONFIG & THEME ----
st.set_page_config(page_title="Flowen Dashboard", layout="wide")
st.markdown("""
<style>
  .main { background-color: #F9FAFB; }
  [data-testid="stSidebar"] { background-color: #0A2342; }
  [data-testid="stSidebar"] * { color: #FFF; font-size:16px; }
  h1,h2,h3,h4 { color: #1B4965; }
  div[data-testid="metric-container"] { background: #FFF; padding:15px; border-radius:12px; box-shadow:0 2px 4px rgba(0,0,0,0.1); margin-bottom:15px; }
  [data-testid="stExpander"] { background: #F0F4F8; border:1px solid #DCE3EB; border-radius:8px; }
  .stButton > button { background-color:#2CA8D2; color:#FFF; border-radius:8px; padding:8px 16px; }
</style>
""", unsafe_allow_html=True)

# ---- BRAND COLORS ----
FLOWEN_COLORS = ["#1B4965", "#2CA8D2", "#21B573", "#90E0EF"]

# ---- DATA LOADER ----
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")
df = load_data()

# ---- SIDEBAR: LOGO & NAV & FILTERS & EXPORT ----
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=150)

lang = st.sidebar.selectbox("🌐 Language / ภาษา", ["EN", "TH"], index=0)
menu = st.sidebar.radio("📊 Navigation", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"] )

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), df["region"].unique())
loans   = st.sidebar.multiselect("Loan Type", df["loan_type"].unique(), df["loan_type"].unique())
min_dpd = st.sidebar.slider("Min Days Past Due", 0, int(df["dpd"].max()), 0)

filtered = df[ df["region"].isin(regions) & df["loan_type"].isin(loans) & (df["dpd"] >= min_dpd) ]

# Export functions

def to_excel(data: pd.DataFrame) -> bytes:
    buf = BytesIO()
    data.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()


def to_pdf(data: pd.DataFrame) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    style = getSampleStyleSheet()
    elems = [Paragraph("Flowen Debtor Report", style["Title"]), Spacer(1,12)]
    table_data = [data.columns.tolist()] + data.values.tolist()
    tbl = Table(table_data, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor(FLOWEN_COLORS[1])),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
    ]))
    elems.append(tbl)
    doc.build(elems)
    return buf.getvalue()

st.sidebar.download_button("⬇️ Export Excel", to_excel(filtered), file_name="flowen_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.sidebar.download_button("⬇️ Export PDF", to_pdf(filtered), file_name="flowen_report.pdf", mime="application/pdf")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔔 Notifications")
st.sidebar.write("- New high-risk accounts flagged")
st.sidebar.write("- AI model retrained")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Debtor Profile")
sel_name = st.sidebar.selectbox("Select Debtor", filtered["name"].unique())
selected = df[df["name"] == sel_name].iloc[0]

# ---- MAIN HEADER ----
st.markdown(f"<div style='display:flex; align-items:center; justify-content:space-between;'>
    <h1>Flowen Dashboard</h1>
    <div style='font-size:18px; color:#1B4965;'>Language: {lang}</div>
</div><hr>", unsafe_allow_html=True)

# ---- UTIL: CARD WRAPPER ----
def card():
    return st.container()

# ---- PAGES ----
if menu == "Risk Overview":
    with card():
        st.subheader("Real-Time Status Panel")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Accounts Contacted Today", "1,203")
        c2.metric("Responses Received", "645")
        c3.metric("Active Conversations", "53")
        c4.metric("Paid Within 24h", "32%")

    with card():
        st.subheader("AI Suggestion Feed")
        top5 = filtered.nlargest(5, "ai_risk_score")
        st.table(top5[["account_id","name","risk_score","loan_type","contact_channel"]]
                  .rename(columns=str.title))

    with card():
        st.subheader("Risk Distribution")
        dist = filtered["risk_level"].value_counts().reset_index()
        dist.columns = ["Risk Level","Count"]
        fig = px.pie(dist, names="Risk Level", values="Count", hole=0.4,
                     color_discrete_sequence=FLOWEN_COLORS)
        st.plotly_chart(fig, use_container_width=True)

    with card():
        st.subheader("Debtor Profile View")
        st.markdown(f"**Name:** {selected['name']}  \\**ID:** {selected['account_id']}")
        st.markdown(f"**Risk Score:** {selected['risk_score']} | **DPD:** {selected['dpd']} days")
        st.markdown(f"**Outstanding:** ฿{selected['total_debt']:,} | **Loan Type:** {selected['loan_type']}")
        st.markdown(f"**Region:** {selected['region']} | **Channel:** {selected['contact_channel']}")

elif menu == "Journey Management":
    with card():
        st.subheader("Journey Funnel Overview")
        funnel = pd.DataFrame({
            "Stage":["Uncontacted","Contacted","Promise to Pay","Paid"],
            "Count":[8500,5200,2100,865]
        })
        fig = px.funnel(funnel, x="Count", y="Stage", color_discrete_sequence=FLOWEN_COLORS)
        st.plotly_chart(fig, use_container_width=True)

    with card():
        st.subheader("Journey Type Performance")
        jm = pd.DataFrame({"Journey":["LINE A","LINE B","Voice","Manual"],
                           "ConvRate%": [31,42,38,28],
                           "AvgDays":[4.2,3.5,4.0,6.1]})
        st.dataframe(jm)

elif menu == "Recovery KPI":
    with card():
        st.subheader("Recovery Overview (MTD)")
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Total Recovered","฿12.8M")
        m2.metric("Recovery Rate","65%")
        m3.metric("Avg Time to Recovery","3.6 days")
        m4.metric("Active Collectors","12")

    with card():
        st.subheader("Daily Recovery Trend")
        trend = pd.DataFrame({"Date":pd.date_range("2025-07-01",7),
                              "Recovered":[1.0,1.2,1.3,1.1,1.5,1.6,1.7]})
        fig = px.line(trend, x="Date", y="Recovered", markers=True,
                      color_discrete_sequence=[FLOWEN_COLORS[1]])
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Behavioral Insights":
    with card():
        st.subheader("Response Behavior")
        rb = filtered["response_behavior"].value_counts().reset_index()
        rb.columns=["Behavior","Count"]
        fig = px.pie(rb, names="Behavior", values="Count", hole=0.4,
                     color_discrete_sequence=FLOWEN_COLORS)
        st.plotly_chart(fig, use_container_width=True)

    with card():
        st.subheader("Monthly Income Distribution")
        fig2 = px.histogram(filtered, x="monthly_income", nbins=30,
                            color_discrete_sequence=[FLOWEN_COLORS[2]])
        st.plotly_chart(fig2, use_container_width=True)

    with card():
        st.subheader("Channel vs Behavior")
        cb = filtered.groupby(["contact_channel","response_behavior"]).size().reset_index(name="Count")
        fig3 = px.bar(cb, x="contact_channel", y="Count", color="response_behavior",
                      barmode="group", color_discrete_sequence=FLOWEN_COLORS)
        st.plotly_chart(fig3, use_container_width=True)
```
