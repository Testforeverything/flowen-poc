import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Custom Theme Colors ───
flowen_colors = ["#00B894", "#00A2C2", "#0984E3"]

# ─── Page Config ───
st.set_page_config(page_title="Flowen: Recovery KPI", layout="wide")
st.title("📊 Recovery KPI Dashboard")

# ─── Load Data ───
@st.cache_data
def load_data():
    df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
    df["status_paid"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else ("In Progress" if x < 30 else "Stuck"))
    if "journey_type" not in df.columns:
        def map_journey(row):
            if row["risk_level"] == "High":
                return "Hardship Assistance"
            elif row["contact_channel"] == "LINE":
                return "Default Prevention"
            elif row["contact_channel"] == "Call":
                return "Promise to Pay Reinforcement"
            else:
                return "General Follow-up"
        df["journey_type"] = df.apply(map_journey, axis=1)
    return df

df = load_data()

# ─── KPI Overview ───
st.markdown("### 📈 Recovery Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Paid Accounts", f"{df[df['dpd'] == 0].shape[0]:,}")
col2.metric("Recovery Rate", f"{(df[df['dpd'] == 0].shape[0] / len(df) * 100):.1f}%")
col3.metric("Avg. DPD of Paid", f"{df[df['dpd'] == 0]['dpd'].mean():.1f} Days")
col4.metric("Unpaid > 30 DPD", f"{df[df['dpd'] > 30].shape[0]:,}")

# ─── Recovery Funnel ───
st.markdown("### 🔄 Recovery Journey Funnel")
funnel_data = pd.DataFrame({
    "Stage": ["Messaged", "Opened", "Responded", "Promised to Pay", "Paid"],
    "Count": [
        len(df),
        df[df["response_behavior"] != "Silent"].shape[0],
        df[df["response_behavior"].isin(["Responsive", "Slow"])].shape[0],
        df[df["status_paid"] == "In Progress"].shape[0],
        df[df["status_paid"] == "Paid"].shape[0]
    ]
})
fig_funnel = px.funnel(
    funnel_data,
    x="Count",
    y="Stage",
    title="End-to-End Recovery Funnel",
    color_discrete_sequence=flowen_colors
)
st.plotly_chart(fig_funnel, use_container_width=True)

# ─── Recovery by Channel ───
st.markdown("### 📡 Channel Effectiveness")
channel_data = df.groupby("contact_channel")["status_paid"].value_counts(normalize=True).unstack().fillna(0)
channel_data = channel_data * 100
channel_data = channel_data.reset_index().rename(columns={"Paid": "Success Rate (%)"})
fig_channel = px.bar(
    channel_data,
    x="contact_channel",
    y="Success Rate (%)",
    title="Recovery Rate by Contact Channel",
    color_discrete_sequence=flowen_colors
)
st.plotly_chart(fig_channel, use_container_width=True)

# ─── Recovery by Risk Group ───
st.markdown("### 🧮 Recovery by Risk Level")
recovery_risk = df.groupby("risk_level")["status_paid"].value_counts(normalize=True).unstack().fillna(0) * 100
recovery_risk = recovery_risk.reset_index().rename(columns={"Paid": "Recovery Rate (%)"})
fig_risk = px.bar(
    recovery_risk,
    x="risk_level",
    y="Recovery Rate (%)",
    color="risk_level",
    title="Recovery Rate by Risk Group",
    color_discrete_sequence=flowen_colors
)
st.plotly_chart(fig_risk, use_container_width=True)

# ─── Journey Success Table ───
st.markdown("### 🧭 Journey Type Conversion Rate")
journey_success = df.groupby("journey_type")["status_paid"].value_counts(normalize=True).unstack().fillna(0)
journey_success = journey_success.reset_index()
journey_success["Paid"] = (journey_success["Paid"] * 100).round(1)
st.dataframe(journey_success[["journey_type", "Paid"]].rename(columns={"journey_type": "Journey Type", "Paid": "Conversion Rate (%)"}))

# ─── Insight Panel ───
st.markdown("### 💡 AI Recovery Insight")
st.info("""
- LINE Reminder B shows **highest ROI** among medium-risk group
- Voice Call still effective for ignored accounts >30 DPD
- Recommend doubling frequency on accounts with AI score > 0.7
""")
