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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Outstanding", "฿{:,.0f}".format(df["total_debt"].sum()))
    with col2:
        st.metric("Recovery Rate", "65%")
    with col3:
        st.metric("Delinquent Accounts", f"{df.shape[0]:,}")

    # Charts
    risk_dist = df["risk_level"].value_counts()
    fig_pie = px.pie(
        names=risk_dist.index,
        values=risk_dist.values,
        hole=0.4,
        title="Risk Distribution"
    )

    trend_data = pd.DataFrame({
        "Month": ["May", "Jun", "Jul", "Aug", "Sep", "Oct"],
        "Recovered": [200000, 250000, 300000, 350000, 380000, 410000]
    })
    fig_line = px.line(trend_data, x="Month", y="Recovered", title="Recovery Trend")

    col4, col5 = st.columns([2,1])
    with col4:
        st.plotly_chart(fig_line, use_container_width=True)
    with col5:
        st.plotly_chart(fig_pie, use_container_width=True)

    # Table
    st.subheader("📋 Debtor Summary")
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

    # Debtor Profile
    st.subheader("🔍 Debtor Profile Viewer")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"### {debtor['name']} (Account: {debtor['account_id']})")
    st.write(f"**Risk Score:** {debtor['risk_score']} / **Risk Level:** {debtor['risk_level']}")
    st.write(f"**Outstanding:** ฿{debtor['total_debt']:,} | **Days Past Due:** {debtor['dpd']} days")
    st.write(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.write(f"**Contact Channel:** {debtor['contact_channel']}")

    # Feature Importance (mock)
    feature_names = ['dpd', 'last_payment_days_ago', 'monthly_income', 'income_level', 'loan_type']
    importances = [0.28, 0.23, 0.20, 0.17, 0.12]
    fig_imp = go.Figure(go.Bar(x=importances[::-1], y=feature_names[::-1], orientation='h'))
    fig_imp.update_layout(title="Top Factors Contributing to AI Risk Score")
    st.plotly_chart(fig_imp, use_container_width=True)

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
    
