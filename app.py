import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── CUSTOM THEME STYLE ───────────────────────────────────────
st.markdown("""
    <style>
        /* Background */
        .main {
            background-color: #F7FAFC;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0A2342;
        }
        [data-testid="stSidebar"] * {
            color: #FFFFFF;
            font-size: 16px;
        }

        /* Titles */
        h1, h2, h3, h4 {
            color: #0A2342;
        }

        /* Metric cards */
        div[data-testid="metric-container"] {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 5px;
        }

        /* Expander */
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

# ─── LOAD DATA ────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── SIDEBAR ──────────────────────────────────────────────────
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=160)
menu = st.sidebar.radio("📊 Navigation", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# ─── PAGE: RISK OVERVIEW ──────────────────────────────────────
if menu == "Risk Overview":
    st.title("📌 Risk Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted Today", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")

    st.subheader("🔍 AI Suggestion Feed")
    with st.expander("Top 5 Accounts Likely to Pay in 48h"):
        st.table(df.sort_values("ai_risk_score", ascending=False).head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]])

    with st.expander("Accounts Ignored All Contact for 7+ Days"):
        st.dataframe(
            df[df["last_payment_days_ago"] > 30]
            .sort_values("risk_score", ascending=False)
            .head(5)[["account_id", "name", "risk_score", "last_payment_days_ago", "region"]],
            use_container_width=True
        )

    st.subheader("⚖️ Human vs AI Effectiveness")
    st.dataframe(pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    }))

    st.info("🧠 AI last retrained: 2 hours ago | Top new feature: Contact Channel | Next model update in: 22 hours")

    st.subheader("📊 Behavior-Based Segmentation")
    segment_data = df["response_behavior"].value_counts().reset_index()
    fig_segment = px.pie(segment_data, names="index", values="response_behavior", hole=0.4)
    st.plotly_chart(fig_segment, use_container_width=True)

    st.subheader("📌 Loan Type Breakdown")
    loan_dist = df["loan_type"].value_counts().reset_index()
    fig_loan = px.pie(loan_dist, names="index", values="loan_type", hole=0.4)
    st.plotly_chart(fig_loan, use_container_width=True)

    st.subheader("📈 Avg DPD by Age Group")
    df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(age_dpd, x="age_group", y="dpd", labels={"dpd": "Avg DPD"})
    st.plotly_chart(fig_age, use_container_width=True)

    st.subheader("📋 Debtor Summary")
    st.dataframe(df[[
        "account_id", "name", "risk_score", "total_debt", "dpd",
        "loan_type", "region", "risk_level"
    ]], use_container_width=True)

# ─── PAGE: JOURNEY MANAGEMENT ─────────────────────────────────
elif menu == "Journey Management":
    st.title("🚀 Journey Management")

    funnel_data = pd.DataFrame({
        "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
        "Count": [8500, 5200, 2100, 865]
    })
    fig_funnel = px.funnel(funnel_data, x="Count", y="Stage")
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.subheader("📊 Journey Performance")
    st.dataframe(pd.DataFrame({
        "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Prompt", "Manual Call"],
        "Conversion Rate (%)": [31, 42, 38, 28],
        "Avg Days to Pay": [4.2, 3.5, 4.0, 6.1]
    }))

    st.subheader("⏱️ Time in Journey by Risk Level")
    fig_time = px.bar(pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High"],
        "Avg Days": [2.5, 4.2, 6.7]
    }), x="Risk Level", y="Avg Days", color="Risk Level")
    st.plotly_chart(fig_time, use_container_width=True)

    st.warning("⚠ 5 accounts have not responded in over 30 days.")
    st.dataframe(df[df["dpd"] > 30].sort_values("last_payment_days_ago", ascending=False).head(5)[[
        "account_id", "name", "dpd", "risk_level", "last_payment_days_ago", "contact_channel"
    ]], use_container_width=True)

# ─── PAGE: RECOVERY KPI ──────────────────────────────────────
elif menu == "Recovery KPI":
    st.title("💰 Recovery KPI")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Recovered", "฿12,850,000")
    col2.metric("Recovery Rate", "64.7%")
    col3.metric("Avg. Time to Recovery", "3.6 days")
    col4.metric("Active Collectors", "12")

    st.subheader("📈 Daily Recovery Trend")
    trend_data = pd.DataFrame({
        "Date": pd.date_range("2025-07-01", periods=10, freq="D"),
        "Recovered": [1000000, 1250000, 1380000, 1220000, 1500000, 1600000, 1700000, 1450000, 1550000, 1650000]
    })
    fig_trend = px.line(trend_data, x="Date", y="Recovered", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("📊 Channel Effectiveness")
    channel_perf = pd.DataFrame({
        "Channel": ["LINE Bot", "Voice Bot", "Phone Call", "Email"],
        "Success Rate (%)": [43, 38, 54, 22],
        "Avg Recovery per Case": [850, 720, 1100, 460]
    })
    fig_bar = px.bar(channel_perf, x="Channel", y="Success Rate (%)", color="Channel")
    st.plotly_chart(fig_bar, use_container_width=True)

# ─── PAGE: BEHAVIORAL INSIGHTS ───────────────────────────────
elif menu == "Behavioral Insights":
    st.title("🧠 Behavioral Insights")

    st.subheader("🎯 Response Behavior")
    response_counts = df["response_behavior"].value_counts().reset_index()
    fig_response = px.pie(response_counts, names="index", values="response_behavior", hole=0.4)
    st.plotly_chart(fig_response, use_container_width=True)

    st.subheader("⏱️ Repayment Timing")
    repay_delay = pd.DataFrame({
        "Delay (Days)": ["0–1", "2–3", "4–7", "8–14", "15+"],
        "Paid Count": [350, 420, 300, 180, 90]
    })
    fig_repay = px.bar(repay_delay, x="Delay (Days)", y="Paid Count")
    st.plotly_chart(fig_repay, use_container_width=True)

    st.subheader("📍 Avoidance by Region")
    avoid = df[df["response_behavior"] == "Ignored"].groupby("region").size().reset_index(name="Ignored Count")
    fig_avoid = px.bar(avoid, x="region", y="Ignored Count", color="region")
    st.plotly_chart(fig_avoid, use_container_width=True)

    st.subheader("💸 Monthly Income Distribution")
    fig_cash = px.histogram(df, x="monthly_income", nbins=30)
    st.plotly_chart(fig_cash, use_container_width=True)

    st.subheader("📡 Channel vs Behavior")
    chan_beh = df.groupby(["contact_channel", "response_behavior"]).size().reset_index(name="Count")
    fig_chan = px.bar(chan_beh, x="contact_channel", y="Count", color="response_behavior", barmode="group")
    st.plotly_chart(fig_chan, use_container_width=True)
