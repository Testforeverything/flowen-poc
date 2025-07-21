# 📄 pages/2_Journey_Management.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Flowen: Journey Management", layout="wide")

# ─── Load Data ────────────────────────────────
@st.cache_data

def load_data():
    df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
    df["status_paid"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else "In Progress" if x < 30 else "Stuck")
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    if "journey_type" not in df.columns:
        df["journey_type"] = df["risk_level"].map({
            "High": "Hardship Assistance",
            "Medium": "Promise to Pay",
            "Low": "Default Prevention"
        })
    return df

df = load_data()

st.title("🧭 Journey Management")

# ─── Funnel Overview ───────────────────────────
st.markdown("### 📶 Journey Funnel")
funnel = pd.DataFrame({
    "Stage": ["Start", "Contacted", "Response", "Promise to Pay", "Paid"],
    "Count": [len(df),
              df[df["response_behavior"] != "No Response"].shape[0],
              df[df["response_behavior"] != "No Response"].shape[0],
              df[df["response_behavior"] == "Promise to Pay"].shape[0],
              df[df["dpd"] == 0].shape[0]]
})
fig = px.funnel(funnel, x="Count", y="Stage", color_discrete_sequence=["#00A2C2"])
st.plotly_chart(fig, use_container_width=True)

# ─── AI Journey Suggestion ─────────────────────
st.markdown("### 🤖 AI Journey Recommendation")

ai_suggestion = df.sample(5)[[
    "account_id", "name", "risk_level", "ai_risk_score", "journey_type", "ai_confidence"
]]
ai_suggestion = ai_suggestion.rename(columns={
    "journey_type": "AI Recommended Journey",
    "ai_confidence": "Confidence (%)"
})
st.dataframe(ai_suggestion, use_container_width=True)

# ─── Journey Log (mock) ────────────────────────
st.markdown("### 📒 Journey Log")
log_df = df.sample(10)[[
    "account_id", "name", "risk_level", "dpd", "journey_type", "response_behavior"
]].rename(columns={
    "journey_type": "Journey Applied",
    "response_behavior": "Debtor Response"
})
st.dataframe(log_df, use_container_width=True)

# ─── Manual Journey Selector ───────────────────
st.markdown("### 🎯 Select Journey Template")
selected_risk = st.selectbox("Select Risk Level", options=df["risk_level"].unique())
selected_template = st.radio("Choose Template", options=[
    "Default Prevention", "Promise to Pay", "Hardship Assistance"
])

st.success(f"For Risk Level '{selected_risk}', template '{selected_template}' is selected.")

# ─── Explanation Card ──────────────────────────
st.info("\nThe selected template is based on AI clustering and past response behavior of similar debtor groups.\n")
