# Flowen: Debt Collection AI Dashboard (Full Layout & Theme)
# - Thai/English toggle
# - Logo Top-Left
# - Professional color scheme (dark blue, teal, light blue, white)

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Config ---
st.set_page_config(layout="wide", page_title="Flowen Dashboard", page_icon="https://i.imgur.com/UOa1y7O.png")

# --- Load Data ---
@st.cache_data

def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# --- Language Toggle ---
lang = st.sidebar.radio("Language / ภาษา", ["EN", "TH"])
def t(en, th):
    return en if lang == "EN" else th

# --- Logo Top ---
st.markdown(
    f"""
    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
        <img src='https://i.imgur.com/UOa1y7O.png' width='50' style='margin-right: 10px;'/>
        <h1 style='margin: 0; font-size: 1.8rem;'>{t("Flowen: Debt Collection AI Dashboard", "Flowen: แพลตฟอร์มติดตามหนี้อัจฉริยะ")}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=140)
menu = st.sidebar.radio(t("Navigation", "เมนูหลัก"), [
    t("Risk Overview", "ภาพรวมความเสี่ยง"),
    t("Journey Management", "จัดการเส้นทางลูกหนี้"),
    t("Recovery KPI", "ตัวชี้วัดการติดตามหนี้"),
    t("Behavioral Insights", "พฤติกรรมลูกหนี้")
])

# --- Main Views ---
if menu.startswith("Risk") or menu.startswith("ภาพรวม"):
    st.subheader(t("Real-Time Status Panel", "สถิติแบบเรียลไทม์"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("Accounts Contacted Today", "จำนวนที่ติดต่อวันนี้"), "1,203")
    c2.metric(t("Responses Received", "ได้รับการตอบกลับ"), "645")
    c3.metric(t("Active Conversations", "การสนทนาที่ดำเนินอยู่"), "53")
    c4.metric(t("Paid Within 24h", "จ่ายภายใน 24 ชม."), "32%")

    st.subheader(t("AI Suggestion Feed", "คำแนะนำจาก AI"))
    with st.expander(t("Top 5 Accounts Likely to Pay in 48h", "ลูกหนี้ที่มีแนวโน้มชำระภายใน 48 ชม.")):
        st.table(df.sort_values("ai_risk_score", ascending=False)
                   .head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]]
                   .rename(columns={
                        "account_id": t("Account ID", "รหัสบัญชี"),
                        "name": t("Name", "ชื่อ"),
                        "risk_score": t("Risk Score", "คะแนนความเสี่ยง"),
                        "loan_type": t("Loan Type", "ประเภทเงินกู้"),
                        "contact_channel": t("Channel", "ช่องทาง")
                   }))

    st.subheader(t("Debtor Segment Overview", "กลุ่มลูกหนี้ตามพฤติกรรม"))
    seg = df["response_behavior"].value_counts().reset_index()
    seg.columns = ["Segment", "Count"]
    fig_seg = px.pie(seg, names="Segment", values="Count", hole=0.4)
    st.plotly_chart(fig_seg, use_container_width=True)

    st.subheader(t("Loan Type Distribution", "การกระจายประเภทเงินกู้"))
    loan = df["loan_type"].value_counts().reset_index()
    loan.columns = ["Loan Type", "Count"]
    fig_loan = px.pie(loan, names="Loan Type", values="Count", hole=0.4)
    st.plotly_chart(fig_loan, use_container_width=True)

    st.subheader(t("Payment Delay by Age Group", "ความล่าช้าตามช่วงอายุ"))
    df["age_group"] = pd.cut(df["age"].astype(int), [0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    ag = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_ag = px.bar(ag, x="age_group", y="dpd", color="age_group",
                    labels={"dpd": t("Avg DPD", "จำนวนวันโดยเฉลี่ย")},
                    title=t("Average Days Past Due by Age Group", "จำนวนวันค้างชำระเฉลี่ยตามช่วงอายุ"))
    st.plotly_chart(fig_ag, use_container_width=True)

elif menu.startswith("Journey") or menu.startswith("จัดการ"):
    st.subheader(t("Customer Funnel", "เส้นทางลูกหนี้"))
    funnel = pd.DataFrame({"Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
                           "Count": [8500, 5200, 2100, 865]})
    fig_funnel = px.bar(funnel, x="Count", y="Stage", orientation="h")
    st.plotly_chart(fig_funnel, use_container_width=True)

elif menu.startswith("Recovery") or menu.startswith("ตัวชี้วัด"):
    st.subheader(t("Total Recovery Rate", "อัตราการกู้คืนทั้งหมด"))
    st.metric("", "65%")
    st.subheader(t("Channel Success Rate", "อัตราสำเร็จของแต่ละช่องทาง"))
    channels = pd.DataFrame({"Channel": ["LINE", "Phone", "Email"], "Success": [60, 54, 47]})
    fig_channel = px.bar(channels, x="Channel", y="Success", color="Channel")
    st.plotly_chart(fig_channel, use_container_width=True)

elif menu.startswith("Behavioral") or menu.startswith("พฤติกรรม"):
    st.subheader(t("Loan Type Distribution", "ประเภทเงินกู้"))
    loan = df["loan_type"].value_counts().reset_index()
    loan.columns = ["Loan Type", "Count"]
    st.plotly_chart(px.pie(loan, names="Loan Type", values="Count", hole=0.4), use_container_width=True)

    st.subheader(t("Success Rate by Age Group", "อัตราสำเร็จตามอายุ"))
    age = pd.cut(df["age"].astype(int), [0, 29, 39, 49, 100], labels=["18–29", "30–39", "40–49", "50+"])
    success = df.assign(age_group=age).groupby("age_group")["ai_risk_score"].mean().reset_index()
    fig = px.bar(success, x="age_group", y="ai_risk_score", labels={"ai_risk_score": t("Success Rate", "อัตราสำเร็จ")})
    st.plotly_chart(fig, use_container_width=True)
