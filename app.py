import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --- Page Config ---
st.set_page_config(page_title="Flowen: Risk Overview", layout="wide")

# --- Load Logo and Display ---
def get_base64_logo(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_logo("ChatGPT Image Jun 21, 2025 at 10_54_37 AM.png")
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="130"/>
    </div>
    """, unsafe_allow_html=True
)

# --- Sidebar Navigation ---
language = st.sidebar.radio("🌐 Language", ["🇬🇧 English", "🇹🇭 ภาษาไทย"])
page = st.sidebar.radio("Menu", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# --- Notification Banner (Mock Realtime) ---
st.markdown(
    """
    <div style="background-color:#0A2342; padding: 10px; border-radius: 8px; color: white; font-weight: bold;">
        📢 Notification: New payment received from Account #10238 (฿1,200)
    </div>
    """, unsafe_allow_html=True
)

# --- Risk Overview Page ---
if page == "Risk Overview":
    st.title("📊 Risk Overview")

    # Real-Time Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")

    st.markdown("---")

    # AI Suggestion
    st.subheader("🧠 Top 5 Accounts Likely to Pay (48h)")
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

    st.subheader("🚨 Accounts Ignored 7+ Days")
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

    st.markdown("---")

    # Pie Chart with Flowen Theme
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(
        segment_data,
        names="Segment",
        values="Count",
        hole=0.4,
        title="Behavior-Based Segmentation",
        color_discrete_sequence=["#2EB3A0", "#1C88E5", "#0A2342", "#7FDBFF", "#39CCCC"]
    )
    st.plotly_chart(fig_segment, use_container_width=True)

    # Debtor Profile View
    st.markdown("### 👤 Debtor Profile View")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")

# Optional: Add `elif` for other pages later (Journey Management, Recovery KPI, etc.)
