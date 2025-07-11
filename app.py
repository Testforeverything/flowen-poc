import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --- Page Setup ---
st.set_page_config(page_title="Flowen: Risk Overview", layout="wide")

# --- Custom CSS for Card Layout ---
st.markdown("""
<style>
.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border: 1px solid #E0E0E0;
    margin-bottom: 20px;
}
[data-testid="metric-container"] {
    background-color: white;
    padding: 10px;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# --- Load Logo ---
def get_base64_logo(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# --- Sidebar ---
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="130"/>
    </div>
""", unsafe_allow_html=True)

language = st.sidebar.radio("🌐 Language", ["🇬🇧 English", "🇹🇭 ภาษาไทย"])
menu = st.sidebar.radio("📂 Menu", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# --- Risk Overview Page ---
if menu == "Risk Overview":
    st.title("📊 Risk Overview")

    # --- Metrics Cards ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Top Accounts Section ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Inactive Accounts ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Pie Chart Segment ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Behavior-Based Segmentation")
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(
        segment_data,
        names="Segment",
        values="Count",
        hole=0.4,
        color_discrete_sequence=["#2EB3A0", "#1C88E5", "#0A2342", "#7FDBFF", "#39CCCC"]
    )
    st.plotly_chart(fig_segment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Debtor Profile View ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Debtor Profile View")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")
    st.markdown('</div>', unsafe_allow_html=True)
