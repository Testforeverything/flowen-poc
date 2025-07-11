import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Flowen: Debt Collection AI Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# Sidebar menu
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=150)
menu = st.sidebar.radio("Navigation", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# --- Risk Overview ---

if menu == "Risk Overview":
    st.title("📊 Risk Overview")

    # --- Real-Time Status Panel ---
    st.markdown("###  Real-Time Status Panel")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Accounts Contacted Today", "1,203")
    col2.metric(" Responses Received", "645")
    col3.metric(" Active Conversations", "53")
    col4.metric(" Paid Within 24h", "32%")

    # --- AI Suggestion Feed ---
    st.markdown("###  AI Suggestion Feed")
    with st.expander("Top 5 Accounts Likely to Pay in 48h"):
        st.table(
            df.sort_values("ai_risk_score", ascending=False)
              .head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]]
              .rename(columns={
                  "account_id": "Account ID",
                  "name": "Name",
                  "risk_score": "Risk Score",
                  "loan_type": "Loan Type",
                  "contact_channel": "Contact Channel"
              })
        )

    with st.expander("Accounts Ignored All Contact for 7+ Days"):
        inactive = df[df["last_payment_days_ago"] > 30].sort_values("risk_score", ascending=False)
        st.dataframe(
            inactive[["account_id", "name", "risk_score", "last_payment_days_ago", "region"]]
            .rename(columns={
                "account_id": "Account ID",
                "name": "Name",
                "risk_score": "Risk Score",
                "last_payment_days_ago": "Last Payment (Days Ago)",
                "region": "Region"
            }).head(5),
            use_container_width=True
        )

    # --- Human vs AI Effectiveness Panel ---
    st.markdown("### ⚖️ Human vs AI Effectiveness")
    effect_data = pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    })
    st.dataframe(effect_data)

    # --- AI Self-Learning Indicator ---
    st.markdown("###  AI Self-Learning System")
    st.info(
        "AI last retrained: **2 hours ago**  \n"
        "Top new feature: **Contact Channel**  \n"
        "Next model update in: **22 hours**"
    )

    # --- Debtor Segment Overview ---
    st.markdown("###  Debtor Segment Overview")
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(segment_data, names="Segment", values="Count", hole=0.4, title="Behavior-Based Segmentation")
    st.plotly_chart(fig_segment, use_container_width=True)

    # --- Loan Type Distribution ---
    st.markdown("###  Loan Type Distribution")
    loan_dist = df["loan_type"].value_counts().reset_index()
    loan_dist.columns = ["Loan Type", "Count"]
    fig_loan = px.pie(
        loan_dist,
        names="Loan Type",
        values="Count",
        title="Loan Type Breakdown",
        hole=0.4
    )
    st.plotly_chart(fig_loan, use_container_width=True)

    # --- Payment Behavior by Age Group ---
    st.markdown("###  Payment Delay by Age Group")
    df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(
        age_dpd,
        x="age_group",
        y="dpd",
        title="Average Days Past Due by Age Group",
        labels={"dpd": "Avg DPD", "age_group": "Age Group"}
    )
    st.plotly_chart(fig_age, use_container_width=True)

    # --- Debtor Summary Table ---
    st.markdown("###  Debtor Summary")
    st.dataframe(df[[
        "account_id", "name", "risk_score", "total_debt", "dpd",
        "loan_type", "region", "risk_level"
    ]].rename(columns={
        "account_id": "Account ID",
        "name": "Name",
        "risk_score": "Risk Score",
        "total_debt": "Outstanding (฿)",
        "dpd": "Days Past Due",
        "loan_type": "Loan Type",
        "region": "Region",
        "risk_level": "Risk Level"
    }), use_container_width=True)

    # --- Debtor Profile Viewer ---
    st.markdown("###  Debtor Profile Viewer")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")

# --- Journey Management ---
elif menu == "Journey Management":
    st.title("📦 Journey Management Dashboard")

    # --- Journey Funnel Overview ---
    st.markdown("### 🔁 Journey Funnel Overview")
    funnel_data = pd.DataFrame({
        "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
        "Count": [8500, 5200, 2100, 865]
    })
    fig_funnel = px.funnel(funnel_data, x="Count", y="Stage", title="Debtor Funnel Progress")
    st.plotly_chart(fig_funnel, use_container_width=True)

    # --- Journey Type Performance ---
    st.markdown("### 📊 Journey Type Performance")
    journey_perf = pd.DataFrame({
        "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Prompt", "Manual Call"],
        "Conversion Rate (%)": [31, 42, 38, 28],
        "Avg Days to Pay": [4.2, 3.5, 4.0, 6.1]
    })
    st.dataframe(journey_perf)

    # --- Time in Journey Distribution ---
    st.markdown("### 🕒 Time in Journey by Risk Level")
    risk_journey_time = pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High"],
        "Avg Days in Journey": [2.5, 4.2, 6.7]
    })
    fig_time = px.bar(
        risk_journey_time,
        x="Risk Level",
        y="Avg Days in Journey",
        color="Risk Level",
        title="Average Time in Journey"
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # --- Stuck Accounts Alert ---
    st.markdown("### 🚥 Stuck Accounts Alert")
    stuck_accounts = df[df["dpd"] > 30].sort_values("last_payment_days_ago", ascending=False).head(5)
    st.warning(f"⚠️ {stuck_accounts.shape[0]} accounts have not responded in over 30 days.")
    st.dataframe(
        stuck_accounts[[
            "account_id", "name", "dpd", "risk_level",
            "last_payment_days_ago", "contact_channel"
        ]].rename(columns={
            "account_id": "Account ID",
            "name": "Name",
            "dpd": "Days Past Due",
            "risk_level": "Risk Level",
            "last_payment_days_ago": "Last Payment (Days Ago)",
            "contact_channel": "Contact Channel"
        }),
        use_container_width=True
    )

    # --- AI Journey Recommendation (Mock) ---
    st.markdown("### 🤖 AI Journey Recommendation (Sample)")
    rec_sample = df.sample(5)[["account_id", "name", "risk_level", "response_behavior"]].copy()
    rec_sample["AI Recommended Journey"] = rec_sample["risk_level"].map({
        "Low": "LINE Reminder A",
        "Medium": "LINE Reminder B",
        "High": "Voice Prompt"
    })
    st.dataframe(
        rec_sample.rename(columns={
            "account_id": "Account ID",
            "name": "Name",
            "risk_level": "Risk Level",
            "response_behavior": "Behavior",
            "AI Recommended Journey": "AI Recommended Journey"
        }),
        use_container_width=True
    )

# --- Recovery KPI ---
elif menu == "Recovery KPI":
    st.title("📈 Recovery KPI Dashboard")

    # --- KPI Summary ---
    st.markdown("### 📊 Recovery Overview (Month-to-date)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Recovered", "฿12,850,000")
    col2.metric("Recovery Rate", "64.7%")
    col3.metric("Avg. Time to Recovery", "3.6 days")
    col4.metric("Active Collectors", "12")

    # --- Recovery Trend Chart ---
    trend_data = pd.DataFrame({
        "Date": pd.date_range("2025-07-01", periods=10, freq="D"),
        "Recovered": [1000000, 1250000, 1380000, 1220000, 1500000, 1600000, 1700000, 1450000, 1550000, 1650000]
    })
    fig_trend = px.line(trend_data, x="Date", y="Recovered", markers=True, title="Daily Recovery Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

    # --- Channel Effectiveness ---
    st.markdown("### 📞 Channel Effectiveness")
    channel_perf = pd.DataFrame({
        "Channel": ["LINE Bot", "Voice Bot", "Phone Call", "Email"],
        "Success Rate (%)": [43, 38, 54, 22],
        "Avg Recovery per Case": [850, 720, 1100, 460]
    })
    fig_bar = px.bar(
        channel_perf,
        x="Channel",
        y="Success Rate (%)",
        color="Channel",
        title="Channel Success Rate"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Collector Performance ---
    st.markdown("### 🧍 Collector Leaderboard")
    collector_data = pd.DataFrame({
        "Collector": ["Aon", "May", "Bee", "Tarn", "Jib"],
        "Recovered (฿)": [1450000, 1380000, 1250000, 1190000, 950000],
        "Cases Closed": [95, 87, 81, 74, 66]
    })
    st.dataframe(collector_data)

    # --- Segment Recovery Overview ---
    st.markdown("### 🧠 Recovery by Risk Level")
    risk_seg = pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High"],
        "Recovery Rate (%)": [72, 63, 44]
    })
    fig_seg = px.bar(
        risk_seg,
        x="Risk Level",
        y="Recovery Rate (%)",
        color="Risk Level",
        title="Recovery Rate by Risk Group"
    )
    st.plotly_chart(fig_seg, use_container_width=True)

    # --- Recovery Funnel ---
    st.markdown("### 🔁 Recovery Conversion Funnel")
    funnel_data = pd.DataFrame({
        "Stage": ["Messaged", "Opened", "Responded", "Promised to Pay", "Paid"],
        "Count": [18000, 14400, 9100, 3400, 1850]
    })
    fig_funnel = px.funnel(
        funnel_data,
        x="Count",
        y="Stage",
        title="End-to-End Recovery Funnel"
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    # --- AI Journey Effectiveness Insight ---
    st.markdown("### 🤖 AI Journey Effectiveness")
    ai_journey = pd.DataFrame({
        "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Push", "Aggressive Call"],
        "Recovery Rate (%)": [28, 42, 38, 35],
        "Best Segment": ["Low Risk", "Medium Risk", "High Risk", "Ignored Group"]
    })
    st.dataframe(ai_journey)

    st.success("✅ Insight: LINE Reminder B has 42% recovery rate in Medium-Risk group. Consider promoting this journey.")


# --- Behavioral Insights ---
elif menu == "Behavioral Insights":
    st.subheader("👥 Behavioral Insights")

    # 1. Response Behavior (Pie Chart)
    st.markdown("###  Response Behavior")
    response_counts = df["response_behavior"].value_counts()
    fig_response = px.pie(
        names=response_counts.index,
        values=response_counts.values,
        title="Customer Response Behavior",
        hole=0.4
    )
    st.plotly_chart(fig_response, use_container_width=True)

    # 2. Repayment Frequency (Bar Chart)
    st.markdown("###  Repayment Frequency")
    repay_freq = df["payment_frequency"].value_counts().reset_index()
    repay_freq.columns = ["Frequency", "Count"]
    fig_freq = px.bar(
        repay_freq,
        x="Frequency",
        y="Count",
        color="Frequency",
        title="Repayment Frequency Distribution"
    )
    st.plotly_chart(fig_freq, use_container_width=True)

    # 3. Avoidance Pattern by Region (Bar Chart)
    st.markdown("###  Avoidance Pattern by Region")
    avoid_pattern = df[df["response_behavior"] == "Ignored"].groupby("region").size().reset_index(name="Ignored Count")
    fig_avoid = px.bar(
        avoid_pattern,
        x="region",
        y="Ignored Count",
        color="region",
        title="Avoidance Pattern by Region"
    )
    st.plotly_chart(fig_avoid, use_container_width=True)

    # 4. Cash Flow Pattern (Histogram)
    st.markdown("###  Cash Flow Pattern (Monthly Income)")
    fig_income = px.histogram(
        df,
        x="monthly_income",
        nbins=30,
        title="Distribution of Monthly Income"
    )
    st.plotly_chart(fig_income, use_container_width=True)

    # 5. Personalization Feedback – Channel Effectiveness (Pie Chart)
    st.markdown("###  Personalization Feedback – Channel Effectiveness")
    channel_perf = df["contact_channel"].value_counts().reset_index()
    channel_perf.columns = ["Channel", "Count"]
    fig_channel = px.pie(
        channel_perf,
        names="Channel",
        values="Count",
        hole=0.4,
        title="Top Performing Contact Channels"
    )
    st.plotly_chart(fig_channel, use_container_width=True)
    
