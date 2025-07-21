# 📄 pages/1_Risk_Overview.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Flowen: Risk Overview", layout="wide")

flowen_colors = ["#00B894", "#00A2C2", "#0984E3"]

# ─── Load Data ────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
    df["status_paid"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else "In Progress" if x < 30 else "Stuck")
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    if "journey_type" not in df.columns:
        def map_journey(row):
            if row["risk_level"] == "High":
                return "Hardship Assistance"
            elif row["contact_channel"] == "LINE":
                return "Default Prevention"
            elif row["contact_channel"] == "Call":
                return "Promise to Pay"
            else:
                return "General Follow-up"
        df["journey_type"] = df.apply(map_journey, axis=1)
    if "ai_confidence" not in df.columns:
        df["ai_confidence"] = (df["ai_risk_score"] * 100).clip(0, 100)
    return df

df = load_data()

# ─── Dashboard Title ───────────────────────────
st.title("📊 Risk Overview")

# ─── Top KPI Metrics ───────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Accounts Contacted", f"{len(df):,}")
col2.metric("Paid Accounts", f"{df[df['dpd'] == 0].shape[0]:,}")
col3.metric("In Progress", f"{df[df['dpd'].between(1, 29)].shape[0]:,}")
col4.metric("Stuck (DPD ≥ 30)", f"{df[df['dpd'] >= 30].shape[0]:,}")

# ─── AI Suggestion Feed ────────────────────────
st.markdown("### 🤖 AI Suggestions")
with st.expander("Top 5 Accounts Likely to Pay (High Score)"):
    top_accounts = df.sort_values("ai_risk_score", ascending=False).head(5)[[
        "account_id", "name", "risk_score", "loan_type", "contact_channel"
    ]]
    st.dataframe(top_accounts)

# ─── Segmentation Charts ───────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    behavior_seg = df["response_behavior"].value_counts().reset_index()
    behavior_seg.columns = ["Behavior", "Count"]
    fig1 = px.pie(behavior_seg, names="Behavior", values="Count", hole=0.4,
                  color_discrete_sequence=flowen_colors, title="Response Behavior")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    loan_type = df["loan_type"].value_counts().reset_index()
    loan_type.columns = ["Loan Type", "Count"]
    fig2 = px.pie(loan_type, names="Loan Type", values="Count", hole=0.3,
                  color_discrete_sequence=flowen_colors, title="Loan Type Distribution")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    age_group = df.groupby("age_group")["dpd"].mean().reset_index()
    fig3 = px.bar(age_group, x="age_group", y="dpd",
                  color_discrete_sequence=flowen_colors,
                  title="Avg. DPD by Age Group", labels={"dpd": "Days Past Due"})
    st.plotly_chart(fig3, use_container_width=True)

# ─── Risk-Level vs Recovery ─────────────────────
st.markdown("### 📈 Risk vs Recovery Rate")
if "recovered" not in df.columns:
    import numpy as np
    np.random.seed(42)
    df["recovered"] = np.where(df["dpd"] == 0, 1, np.random.binomial(1, 0.6, size=len(df)))

recovery_risk = df.groupby("risk_level")["recovered"].mean().reset_index()
recovery_risk["Recovery Rate (%)"] = recovery_risk["recovered"] * 100
fig4 = px.bar(recovery_risk, x="risk_level", y="Recovery Rate (%)", text="Recovery Rate (%)",
              color="risk_level", color_discrete_sequence=flowen_colors,
              title="Recovery Rate by Risk Level")
fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig4, use_container_width=True)

# ─── Risk vs Journey Type ───────────────────────
st.markdown("### 🧭 Journey Strategy by Risk Group")
journey_risk = df.groupby(["risk_level", "journey_type"]).size().reset_index(name="Count")
fig5 = px.bar(journey_risk, x="risk_level", y="Count", color="journey_type",
              barmode="stack", color_discrete_sequence=flowen_colors,
              title="Journey Allocation by Risk")
st.plotly_chart(fig5, use_container_width=True)

# ─── Debtor Table ──────────────────────────────
st.markdown("### 📋 Debtor Summary Table")
st.dataframe(df[[
    "account_id", "name", "risk_score", "dpd", "risk_level", "journey_type", "loan_type"
]].sort_values("dpd", ascending=False).reset_index(drop=True), use_container_width=True)
