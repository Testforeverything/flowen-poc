import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Config ───
st.set_page_config(page_title="Flowen: Behavioral Insights", layout="wide")
st.title("🧠 Behavioral Insights")

# ─── Load Data ───
@st.cache_data
def load_data():
    df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    return df

df = load_data()

# ─── Summary Cards ───
col1, col2, col3 = st.columns(3)
col1.metric("Behavior Groups", df["clustering_group"].nunique())
col2.metric("Most Common Tag", df["response_behavior"].value_counts().idxmax())
col3.metric("Top Region", df["region"].value_counts().idxmax())

# ─── Clustering Overview ───
st.markdown("### 🔍 Clustering Overview")
cluster_counts = df["clustering_group"].value_counts().reset_index()
cluster_counts.columns = ["Group", "Count"]
fig1 = px.bar(cluster_counts, x="Group", y="Count", color="Group", title="Customer Clustering Distribution")
st.plotly_chart(fig1, use_container_width=True)

# ─── Grouped Behaviors ───
st.markdown("### 📋 Behavior by Cluster")
behavior_group = pd.crosstab(df["clustering_group"], df["response_behavior"], normalize="index") * 100
st.dataframe(behavior_group.round(1), use_container_width=True)

# ─── Risk Level vs. Behavior ───
st.markdown("### 📉 Behavior vs. Risk Level")
risk_behavior = pd.crosstab(df["risk_level"], df["response_behavior"], normalize="index") * 100
fig2 = px.bar(risk_behavior, barmode="group", title="Risk Level vs. Debtor Behavior", labels={"value": "Percentage", "risk_level": "Risk Level"})
st.plotly_chart(fig2, use_container_width=True)

# ─── NLP-Generated Tags Summary ───
st.markdown("### 🏷️ NLP Behavior Tags")
if "nlp_behavior_tag" in df.columns:
    tag_counts = df["nlp_behavior_tag"].value_counts().reset_index()
    tag_counts.columns = ["Behavior Tag", "Count"]
    fig3 = px.pie(tag_counts, names="Behavior Tag", values="Count", hole=0.4, title="Behavior Tag Distribution")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠️ NLP behavior tags not found in data.")

# ─── AI Insight Box ───
st.markdown("### 💬 AI Insight from Behavior")
st.info("""
- Group 3 shows high responsiveness to polite reminders via LINE
- Group 1 has high 'Promise to Pay' tag but low actual payment → consider follow-up within 3 days
- Cluster 5 tends to ignore calls, prefer email or non-intrusive reminders
""")
