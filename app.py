import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧠 Flowen: Debt Collection AI Dashboard")

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
    st.markdown("### 🟢 Real-Time Status Panel")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📍 Accounts Contacted Today", "1,203")
    col2.metric("📩 Responses Received", "645")
    col3.metric("💬 Active Conversations", "53")
    col4.metric("✅ Paid Within 24h", "32%")

    # --- AI Suggestion Feed ---
    st.markdown("### 🤖 AI Suggestion Feed")
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
    st.markdown("### 🔁 AI Self-Learning System")
    st.info(
        "AI last retrained: **2 hours ago**  \n"
        "Top new feature: **Contact Channel**  \n"
        "Next model update in: **22 hours**"
    )

    # --- Debtor Segment Overview ---
    st.markdown("### 👥 Debtor Segment Overview")
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(segment_data, names="Segment", values="Count", hole=0.4, title="Behavior-Based Segmentation")
    st.plotly_chart(fig_segment, use_container_width=True)

    # --- Loan Type Distribution ---
    st.markdown("### 🏦 Loan Type Distribution")
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
    st.markdown("### 👤 Payment Delay by Age Group")
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
    st.markdown("### 📋 Debtor Summary")
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
    st.markdown("### 🔍 Debtor Profile Viewer")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")

# --- Journey Management ---
elif menu == "Journey Management":
    st.subheader("📦 Journey Funnel")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", "21,500")
    col2.metric("Engagement Rate", "70%")
    col3.metric("Active Journeys", "14,450")

    funnel_data = pd.DataFrame({
        "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
        "Count": [12000, 7500, 3200, 1050]
    })
    fig_funnel = px.bar(funnel_data, x="Count", y="Stage", orientation='h', title="Customer Funnel")
    st.plotly_chart(fig_funnel, use_container_width=True)

# --- Recovery KPI ---
elif menu == "Recovery KPI":
    st.subheader("📈 Recovery KPI Overview")
    st.metric("Total Recovery Rate", "65%")

    channel_data = pd.DataFrame({
        "Channel": ["LINE", "Phone", "Email"],
        "Success": [60, 54, 47]
    })
    fig_bar = px.bar(channel_data, x="Channel", y="Success", text="Success", title="Channel Success Rate")
    st.plotly_chart(fig_bar, use_container_width=True)

    daily = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Recovery": [100, 150, 200, 230, 250, 280, 300]
    })
    fig_trend = px.line(daily, x="Day", y="Recovery", markers=True, title="Daily Recovery Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

# --- Behavioral Insights ---
elif menu == "Behavioral Insights":
    st.subheader("👥 Behavioral Insights")

    # 1. Response Behavior (Pie Chart)
    st.markdown("### 📨 Response Behavior")
    response_counts = df["response_behavior"].value_counts()
    fig_response = px.pie(
        names=response_counts.index,
        values=response_counts.values,
        title="Customer Response Behavior",
        hole=0.4
    )
    st.plotly_chart(fig_response, use_container_width=True)

    # 2. Repayment Frequency (Bar Chart)
    st.markdown("### 💸 Repayment Frequency")
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
    st.markdown("### 🚫 Avoidance Pattern by Region")
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
    st.markdown("### 💵 Cash Flow Pattern (Monthly Income)")
    fig_income = px.histogram(
        df,
        x="monthly_income",
        nbins=30,
        title="Distribution of Monthly Income"
    )
    st.plotly_chart(fig_income, use_container_width=True)

    # 5. Personalization Feedback – Channel Effectiveness (Pie Chart)
    st.markdown("### 📢 Personalization Feedback – Channel Effectiveness")
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
    
