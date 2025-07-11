import streamlit as st
import pandas as pd
import plotly.express as px

# ─── PAGE SETUP ───────────────────────────────────────
st.set_page_config(page_title="Flowen: Risk Overview", layout="wide")

# ─── CUSTOM CSS ───────────────────────────────────────
st.markdown("""
<style>
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 18px;
        font-weight: bold;
        color: #0A2342;
        margin-bottom: 12px;
    }
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── LANGUAGE DROPDOWN (TOP RIGHT) ────────────────────
top_left, top_spacer, top_right = st.columns([6, 5, 1.2])
with top_right:
    language = st.selectbox(" ", ["🇬🇧 English", "🇹🇭 ภาษาไทย"], label_visibility="collapsed")

# ─── LOCALIZED TEXT ───────────────────────────────────
TEXT = {
    "title": {
        "🇬🇧 English": "📊 Flowen — Risk Overview",
        "🇹🇭 ภาษาไทย": "📊 ภาพรวมความเสี่ยงของลูกหนี้"
    },
    "metrics": {
        "outstanding": {"🇬🇧 English": "Total Outstanding", "🇹🇭 ภาษาไทย": "ยอดค้างชำระรวม"},
        "recovery": {"🇬🇧 English": "Recovery Rate", "🇹🇭 ภาษาไทย": "อัตราการเก็บเงินสำเร็จ"},
        "journey": {"🇬🇧 English": "Journey Management", "🇹🇭 ภาษาไทย": "การจัดการทวงหนี้"},
    },
    "recovery_trend": {"🇬🇧 English": "Recovery Trend", "🇹🇭 ภาษาไทย": "แนวโน้มการชำระเงิน"},
    "debtor_summary": {"🇬🇧 English": "Debtor Summary", "🇹🇭 ภาษาไทย": "สรุปลูกหนี้"},
    "total_recovery_rate": {"🇬🇧 English": "Total Recovery Rate", "🇹🇭 ภาษาไทย": "อัตราการเก็บรวม"},
    "risk_distribution": {"🇬🇧 English": "Risk Distribution", "🇹🇭 ภาษาไทย": "การกระจายความเสี่ยง"},
    "agent_performance": {"🇬🇧 English": "Agent Performance", "🇹🇭 ภาษาไทย": "ผลการทำงานของเจ้าหน้าที่"},
    "channel_accuracy": {"🇬🇧 English": "Channel Accuracy", "🇹🇭 ภาษาไทย": "ความแม่นยำตามช่องทาง"},
    "loan_type": {"🇬🇧 English": "Loan Type Distribution", "🇹🇭 ภาษาไทย": "ประเภทสินเชื่อ"},
    "reasons": {"🇬🇧 English": "Payment Reason Breakdown", "🇹🇭 ภาษาไทย": "สาเหตุที่ลูกหนี้ไม่จ่าย"}
}

# ─── TITLE ────────────────────────────────────────────
st.title(TEXT["title"][language])

# ─── LAYOUT ───────────────────────────────────────────
col_main, col_right = st.columns([2.5, 1.5])

# ─── LEFT PANEL ───────────────────────────────────────
with col_main:
    col1, col2, col3 = st.columns(3)
    col1.metric(TEXT["metrics"]["outstanding"][language], "฿85,200,000")
    col2.metric(TEXT["metrics"]["recovery"][language], "65%")
    col3.metric(TEXT["metrics"]["journey"][language], "70%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📈 {TEXT['recovery_trend'][language]}</div>", unsafe_allow_html=True)
    trend_data = pd.DataFrame({
        "Month": ["May", "Jun", "Jul", "Aug", "Sep", "Oct"],
        "Total": [220000, 280000, 340000, 400000, 470000, 530000],
        "Paid": [150000, 180000, 220000, 260000, 300000, 360000]
    })
    fig_line = px.line(trend_data, x="Month", y=["Total", "Paid"],
                       markers=True, color_discrete_sequence=["#1C88E5", "#2EB3A0"])
    fig_line.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📋 {TEXT['debtor_summary'][language]}</div>", unsafe_allow_html=True)
    st.dataframe(df[["name", "risk_score", "total_debt", "dpd"]]
        .rename(columns={
            "name": "Customer" if language == "🇬🇧 English" else "ชื่อลูกหนี้",
            "risk_score": "Risk Score" if language == "🇬🇧 English" else "คะแนนความเสี่ยง",
            "total_debt": "Outstanding" if language == "🇬🇧 English" else "ยอดหนี้",
            "dpd": "Days Past Due" if language == "🇬🇧 English" else "เกินกำหนด (วัน)"
        }).head(5), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RIGHT PANEL ──────────────────────────────────────
with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>✅ {TEXT['total_recovery_rate'][language]}</div>", unsafe_allow_html=True)
    donut = pd.DataFrame({"name": ["Recovered", "Remaining"], "value": [65, 35]})
    fig_donut = px.pie(donut, names="name", values="value", hole=0.6,
                       color_discrete_sequence=["#2EB3A0", "#E0E0E0"])
    fig_donut.update_layout(showlegend=False, height=200)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📊 {TEXT['risk_distribution'][language]}</div>", unsafe_allow_html=True)
    pie = pd.DataFrame({"Level": ["Low", "Medium", "High"], "Share": [34, 27, 39]})
    fig_pie = px.pie(pie, names="Level", values="Share",
                     color_discrete_sequence=["#2EB3A0", "#1C88E5", "#0A2342"])
    fig_pie.update_layout(showlegend=True, height=250)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>👩‍💼 {TEXT['agent_performance'][language]}</div>", unsafe_allow_html=True)
    st.markdown("• 🎯 Target: 65%  \n• ✈️ Actual Recovery: 70%  \n• 👥 Agent Avg: 72%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📞 {TEXT['channel_accuracy'][language]}</div>", unsafe_allow_html=True)
    channel = pd.DataFrame({
        "Channel": ["LINE", "Phone", "Email"],
        "Accuracy": [68, 54, 47]
    })
    fig_bar = px.bar(channel, x="Channel", y="Accuracy", text="Accuracy",
                     color="Channel", color_discrete_sequence=["#2EB3A0", "#1C88E5", "#FFD43B"])
    fig_bar.update_layout(height=250, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>💳 {TEXT['loan_type'][language]}</div>", unsafe_allow_html=True)
    loan = pd.DataFrame({"Type": ["Personal Loan", "Auto Loan"], "Share": [52, 48]})
    fig_loan = px.pie(loan, names="Type", values="Share",
                      color_discrete_sequence=["#1C88E5", "#2EB3A0"])
    fig_loan.update_layout(showlegend=True, height=220)
    st.plotly_chart(fig_loan, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📉 {TEXT['reasons'][language]}</div>", unsafe_allow_html=True)
    st.markdown("- Insufficient Funds: 42%  \n- Job Loss: 36%  \n- Debt Overlap: 22%")
    st.markdown('</div>', unsafe_allow_html=True)
