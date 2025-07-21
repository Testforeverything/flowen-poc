import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import BytesIO

# Load and cache the data
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_5000_enhanced.csv")

df = load_data()

# Set Streamlit page config
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# Load and inject logo
with open("flowen_logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
    }}
    .header-logo {{
        height: 50px;
    }}
    .lang-dropdown {{
        font-size: 16px;
        padding: 5px;
    }}
    .card {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }}
</style>
<div class="header-container">
    <img class="header-logo" src="data:image/png;base64,{logo_base64}" />
    <div>
        <select class="lang-dropdown" onchange="window.location.href='?lang=' + this.value">
            <option value="en" {'selected' if st.query_params.get('lang') == 'en' else ''}>🇬🇧 EN</option>
            <option value="th" {'selected' if st.query_params.get('lang') == 'th' else ''}>🇹🇭 TH</option>
        </select>
    </div>
</div>
""", unsafe_allow_html=True)

# Language toggle
lang = st.query_params.get("lang", "en")

# Sidebar
menu = st.sidebar.radio("Navigation", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# Custom CI color
flowen_colors = ["#00B894", "#00A2C2", "#0984E3"]

# Module: Risk Overview
if menu == "Risk Overview":
    st.title("📊 Risk Overview")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Real-Time Status Panel")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accounts Contacted Today", "1,203")
        col2.metric("Responses Received", "645")
        col3.metric("Active Conversations", "53")
        col4.metric("Paid Within 24h", "32%")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("AI Suggestion Feed")
        st.dataframe(
            df.sort_values("ai_risk_score", ascending=False)
              .head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]]
              .rename(columns={
                  "account_id": "Account ID",
                  "name": "Name",
                  "risk_score": "Risk Score",
                  "loan_type": "Loan Type",
                  "contact_channel": "Contact Channel"
              }),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Debtor Segment Overview")
        seg = df["response_behavior"].value_counts().reset_index()
        seg.columns = ["Segment", "Count"]
        fig_seg = px.pie(seg, names="Segment", values="Count", hole=0.4,
                         color_discrete_sequence=flowen_colors)
        st.plotly_chart(fig_seg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Loan Type Distribution")
        loan = df["loan_type"].value_counts().reset_index()
        loan.columns = ["Loan Type", "Count"]
        fig_loan = px.pie(loan, names="Loan Type", values="Count", hole=0.4,
                          color_discrete_sequence=flowen_colors)
        st.plotly_chart(fig_loan, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Payment Delay by Age Group")
        df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
        age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
        fig_age = px.bar(age_dpd, x="age_group", y="dpd", labels={"dpd": "Avg DPD"},
                         color_discrete_sequence=flowen_colors)
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Debtor Profile Viewer")
        selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
        debtor = df[df["account_id"] == selected_account].iloc[0]
        st.markdown(f"""
        **Name:** {debtor['name']}  
        **Account ID:** {debtor['account_id']}  
        **Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}  
        **Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days  
        **Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}  
        **Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ─── Journey Management ─────────────────────────────────────────
elif menu == "Journey Management":
    st.title("🛤️ Journey Management")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Funnel Overview")
        stage_counts = {
            "Uncontacted": len(df[df["last_contact_date"].isna()]),
            "Contacted": len(df[df["last_contact_date"].notna()]),
            "Promise to Pay": len(df[df["response_behavior"] == "Promise to Pay"]),
            "Paid": len(df[df["recovered"] == 1]),
        }
        funnel_df = pd.DataFrame({
            "Stage": list(stage_counts.keys()),
            "Count": list(stage_counts.values())
        })
        funnel_chart = px.funnel(
            funnel_df, x="Count", y="Stage", title="Debtor Journey Funnel",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(funnel_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Journey Type Performance")
        perf_data = pd.DataFrame({
            "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Prompt", "Manual Call"],
            "Conversion Rate (%)": [31, 42, 38, 28],
            "Avg Days to Pay": [4.2, 3.5, 4.0, 6.1]
        })
        st.dataframe(perf_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Avg Time in Journey by Risk Level")
        time_risk = df.groupby("risk_level")["dpd"].mean().reset_index()
        fig_time = px.bar(
            time_risk, x="risk_level", y="dpd",
            title="Average DPD by Risk Level",
            color="risk_level",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Stuck Accounts (No Response > 30 Days)")
        stuck = df[df["dpd"] > 30].sort_values("dpd", ascending=False).head(10)
        st.dataframe(stuck[[
            "account_id", "name", "dpd", "risk_level", "last_payment_days_ago", "contact_channel"
        ]].rename(columns={
            "account_id": "Account ID", "name": "Name", "dpd": "DPD",
            "risk_level": "Risk Level", "last_payment_days_ago": "Last Payment (Days)",
            "contact_channel": "Channel"
        }), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("AI Journey Recommendation")
        sample = df.sample(5).copy()
        sample["AI Journey"] = sample["risk_level"].map({
            "Low": "LINE Reminder A",
            "Medium": "LINE Reminder B",
            "High": "Voice Prompt"
        })
        st.dataframe(sample[[
            "account_id", "name", "risk_level", "response_behavior", "AI Journey"
        ]].rename(columns={
            "account_id": "Account ID", "name": "Name",
            "risk_level": "Risk Level", "response_behavior": "Behavior",
            "AI Journey": "Recommended Journey"
        }), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
elif menu == "Recovery KPI":
    st.title("💰 Recovery KPI")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Recovery Summary (Month-to-date)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Recovered", "฿12,850,000")
        col2.metric("Recovery Rate", "64.7%")
        col3.metric("Avg. Time to Recovery", "3.6 days")
        col4.metric("Active Collectors", "12")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Daily Recovery Trend")
        trend_data = pd.DataFrame({
            "Date": pd.date_range("2025-07-01", periods=10, freq="D"),
            "Recovered": [1000000, 1250000, 1380000, 1220000, 1500000,
                          1600000, 1700000, 1450000, 1550000, 1650000]
        })
        fig_trend = px.line(trend_data, x="Date", y="Recovered", markers=True,
                            title="Daily Recovery Amount", color_discrete_sequence=flowen_colors)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Channel Effectiveness")
        channel_perf = pd.DataFrame({
            "Channel": ["LINE Bot", "Voice Bot", "Phone Call", "Email"],
            "Success Rate (%)": [43, 38, 54, 22],
            "Avg Recovery per Case": [850, 720, 1100, 460]
        })
        fig_channel = px.bar(channel_perf, x="Channel", y="Success Rate (%)", color="Channel",
                             color_discrete_sequence=flowen_colors, title="Channel Success Rate")
        st.plotly_chart(fig_channel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Collector Leaderboard")
        collector_data = pd.DataFrame({
            "Collector": ["Aon", "May", "Bee", "Tarn", "Jib"],
            "Recovered (฿)": [1450000, 1380000, 1250000, 1190000, 950000],
            "Cases Closed": [95, 87, 81, 74, 66]
        })
        st.dataframe(collector_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Recovery by Risk Level")
        risk_seg = pd.DataFrame({
            "Risk Level": ["Low", "Medium", "High"],
            "Recovery Rate (%)": [72, 63, 44]
        })
        fig_risk = px.bar(risk_seg, x="Risk Level", y="Recovery Rate (%)",
                          color="Risk Level", color_discrete_sequence=flowen_colors,
                          title="Recovery Rate by Risk Group")
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Recovery Conversion Funnel")
        funnel_data = pd.DataFrame({
            "Stage": ["Messaged", "Opened", "Responded", "Promised to Pay", "Paid"],
            "Count": [18000, 14400, 9100, 3400, 1850]
        })
        fig_funnel = px.funnel(funnel_data, x="Count", y="Stage", title="End-to-End Recovery Funnel",
                               color_discrete_sequence=flowen_colors)
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("AI Journey Effectiveness Insight")
        ai_journey = pd.DataFrame({
            "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Push", "Aggressive Call"],
            "Recovery Rate (%)": [28, 42, 38, 35],
            "Best Segment": ["Low Risk", "Medium Risk", "High Risk", "Ignored Group"]
        })
        st.dataframe(ai_journey, use_container_width=True)
        st.success("📈 Insight: LINE Reminder B has 42% recovery rate in Medium-Risk group. Consider promoting this journey.")
        st.markdown("</div>", unsafe_allow_html=True)
elif menu == "Behavioral Insights":
    st.title("🧠 Behavioral Insights")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Response Behavior")
        response_counts = df["response_behavior"].value_counts().reset_index()
        response_counts.columns = ["Behavior", "Count"]
        fig_response = px.pie(
            response_counts,
            names="Behavior",
            values="Count",
            hole=0.4,
            title="Customer Response Breakdown",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_response, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Repayment Timing")
        repay_delay = pd.DataFrame({
            "Delay (Days)": ["0–1", "2–3", "4–7", "8–14", "15+"],
            "Paid Count": [350, 420, 300, 180, 90]
        })
        fig_repay = px.bar(
            repay_delay,
            x="Delay (Days)",
            y="Paid Count",
            title="Repayment after Reminder Timing",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_repay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Avoidance Pattern by Region")
        avoid = df[df["response_behavior"] == "Ignored"].groupby("region").size().reset_index(name="Ignored Count")
        fig_avoid = px.bar(
            avoid,
            x="region",
            y="Ignored Count",
            color="region",
            title="Avoidance by Region",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_avoid, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Cash Flow Pattern")
        fig_cash = px.histogram(
            df,
            x="monthly_income",
            nbins=30,
            title="Monthly Income Distribution",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_cash, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Channel vs Behavior")
        chan_beh = df.groupby(["contact_channel", "response_behavior"]).size().reset_index(name="Count")
        fig_chan = px.bar(
            chan_beh,
            x="contact_channel",
            y="Count",
            color="response_behavior",
            barmode="group",
            title="Contact Channel Performance by Behavior",
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_chan, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("AI Insight Panel – NLP Behavior Tags")
        st.info("AI analyzes conversation logs and assigns behavioral tags for smarter journey orchestration.")
        ai_tags = pd.DataFrame({
            "Sample Message": [
                "ขอเลื่อน 3 วัน",
                "ตอนนี้ไม่มีเงิน",
                "ไม่ใช่หนี้ผม",
                "จะจ่ายพรุ่งนี้",
                "ไม่ตอบกลับ"
            ],
            "AI Tag": [
                "Willing",
                "Cashflow_Issue",
                "Dispute",
                "Pay_Intent",
                "Silent"
            ],
            "Recommended Action": [
                "Remind in 2 days",
                "Pause & retry next payday",
                "Send dispute form",
                "Follow-up in 24h",
                "Escalate to voice"
            ]
        })
        st.dataframe(ai_tags, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


