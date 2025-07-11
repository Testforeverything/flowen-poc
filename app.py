import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Flowen: Risk Overview", layout="wide")

# --- LOAD MOCK DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# --- STYLING ---
st.markdown("""
<style>
    .card {
        background-color: white;
        padding: 20px 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
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

# --- LANGUAGE DROPDOWN (TOP RIGHT CORNER) ---
top_left, top_spacer, top_right = st.columns([6, 5, 1.2])
with top_right:
    language = st.selectbox(" ", ["🇬🇧 English", "🇹🇭 ภาษาไทย"], label_visibility="collapsed")

# --- DICTIONARY TRANSLATION ---
T = {
    "title": {"🇬🇧 English": "📊 Flowen — Risk Overview", "🇹🇭 ภาษาไทย": "📊 ภาพรวมความเสี่ยง"},
    "total": {"🇬🇧 English": "Total Outstanding", "🇹🇭 ภาษาไทย": "ยอดหนี้รวม"},
    "recovery": {"🇬🇧 English": "Recovery Rate", "🇹🇭 ภาษาไทย": "อัตราการเก็บเงิน"},
    "journey": {"🇬🇧 English": "Journey Management", "🇹🇭 ภาษาไทย": "การจัดการลูกหนี้"},
    "trend": {"🇬🇧 English": "Recovery Trend", "🇹🇭 ภาษาไทย": "แนวโน้มการเก็บเงิน"},
    "summary": {"🇬🇧 English": "Debtor Summary", "🇹🇭 ภาษาไทย": "สรุปลูกหนี้"},
    "risk": {"🇬🇧 English": "Risk Distribution", "🇹🇭 ภาษาไทย": "การกระจายความเสี่ยง"},
    "agent": {"🇬🇧 English": "Agent Performance", "🇹🇭 ภาษาไทย": "ประสิทธิภาพเจ้าหน้าที่"},
    "channel": {"🇬🇧 English": "Channel Accuracy", "🇹🇭 ภาษาไทย": "ความแม่นยำของช่องทาง"},
    "loan": {"🇬🇧 English": "Loan Type Distribution", "🇹🇭 ภาษาไทย": "สัดส่วนประเภทสินเชื่อ"},
    "reason": {"🇬🇧 English": "Payment Reason Breakdown", "🇹🇭 ภาษาไทย": "เหตุผลที่ไม่ชำระเงิน"},
}

# --- PAGE TITLE ---
st.title(T["title"][language])

# --- 2-COLUMN LAYOUT ---
col_left, col_right = st.columns([2.5, 1.5])

# === LEFT PANEL ===
with col_left:
    col1, col2, col3 = st.columns(3)
    col1.metric(T["total"][language], "฿85,200,000")
    col2.metric(T["recovery"][language], "65%")
    col3.metric(T["journey"][language], "70%")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📈 {T['trend'][language]}</div>", unsafe_allow_html=True)
    trend_df = pd.DataFrame({
        "Month": ["May", "Jun", "Jul", "Aug", "Sep", "Oct"],
        "Collected": [220000, 280000, 340000, 400000, 470000, 530000],
        "Paid": [150000, 180000, 220000, 260000, 300000, 360000]
    })
    fig = px.line(trend_df, x="Month", y=["Collected", "Paid"],
                  markers=True, color_discrete_sequence=["#1C88E5", "#2EB3A0"])
    fig.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📋 {T['summary'][language]}</div>", unsafe_allow_html=True)
    st.dataframe(
        df[["name", "risk_score", "total_debt", "dpd"]]
        .rename(columns={
            "name": "Customer" if language == "🇬🇧 English" else "ชื่อลูกหนี้",
            "risk_score": "Risk Score" if language == "🇬🇧 English" else "คะแนนความเสี่ยง",
            "total_debt": "Outstanding" if language == "🇬🇧 English" else "ยอดหนี้",
            "dpd": "Days Past Due" if language == "🇬🇧 English" else "เกินกำหนด (วัน)"
        }).head(5),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# === RIGHT PANEL ===
with col_right:
    # --- Recovery Donut ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>✅ Total Recovery Rate</div>", unsafe_allow_html=True)
    donut = pd.DataFrame({"Status": ["Recovered", "Remaining"], "Value": [65, 35]})
    fig_donut = px.pie(donut, names="Status", values="Value", hole=0.6,
                       color_discrete_sequence=["#2EB3A0", "#E0E0E0"])
    fig_donut.update_layout(showlegend=False, height=200)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Risk Pie Chart ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📊 {T['risk'][language]}</div>", unsafe_allow_html=True)
    risk_df = pd.DataFrame({"Level": ["Low", "Medium", "High"], "Share": [34, 27, 39]})
    fig_risk = px.pie(risk_df, names="Level", values="Share",
                      color_discrete_sequence=["#2EB3A0", "#1C88E5", "#0A2342"])
    fig_risk.update_layout(showlegend=True, height=250)
    st.plotly_chart(fig_risk, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Agent Performance Text ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>👩‍💼 {T['agent'][language]}</div>", unsafe_allow_html=True)
    st.markdown("• Target: 65%  \n• Actual: 70%  \n• Team Avg: 72%")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Channel Bar Chart ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📞 {T['channel'][language]}</div>", unsafe_allow_html=True)
    channel_df = pd.DataFrame({
        "Channel": ["LINE", "Phone", "Email"],
        "Accuracy": [68, 54, 47]
    })
    fig_channel = px.bar(channel_df, x="Channel", y="Accuracy", text="Accuracy",
                         color="Channel", color_discrete_sequence=["#2EB3A0", "#1C88E5", "#FFD43B"])
    fig_channel.update_layout(height=250, showlegend=False)
    st.plotly_chart(fig_channel, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Loan Type Pie ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>💳 {T['loan'][language]}</div>", unsafe_allow_html=True)
    loan_df = pd.DataFrame({"Type": ["Personal", "Auto"], "Share": [52, 48]})
    fig_loan = px.pie(loan_df, names="Type", values="Share",
                      color_discrete_sequence=["#1C88E5", "#2EB3A0"])
    fig_loan.update_layout(height=220)
    st.plotly_chart(fig_loan, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Payment Reasons Text ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>📉 {T['reason'][language]}</div>", unsafe_allow_html=True)
    st.markdown("- Insufficient Funds: 42%  \n- Job Loss: 36%  \n- Debt Overlap: 22%")
    st.markdown('</div>', unsafe_allow_html=True)
