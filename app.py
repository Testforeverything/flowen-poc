import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ----- Load Logo -----
def get_logo_base64(path="flowen_logo.png"):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_logo_base64()

# ----- Load Data -----
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ----- Language Toggle -----
lang_options = {"🇬🇧 EN": "en", "🇹🇭 TH": "th"}
lang = st.selectbox("", options=list(lang_options.keys()), index=0, key="lang_select", 
                    label_visibility="collapsed")

# ----- CSS Style -----
st.markdown(f"""
<style>
/* Background and font */
body {{
    background-color: #F8FAFC;
    font-family: 'Segoe UI', sans-serif;
}}

/* Logo at top-left */
#logo-container {{
    position: fixed;
    top: 15px;
    left: 20px;
    z-index: 100;
}}

/* Card container */
.card {{
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    padding: 20px;
    margin-bottom: 20px;
}}

/* Align language flag top-right */
div[data-testid="stSelectbox"] {{
    position: absolute;
    top: 15px;
    right: 30px;
    z-index: 100;
}}
</style>

<div id="logo-container">
    <img src="data:image/png;base64,{logo_base64}" width="120">
</div>
""", unsafe_allow_html=True)

# ----- Sidebar Navigation -----
st.sidebar.title("Navigation")
section = st.sidebar.radio("", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# ----- Set Color Template -----
flowen_colors = px.colors.sequential.Tealgrn  # Green → Blue tone

# ----- Page: Risk Overview -----
if section == "Risk Overview":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Real-Time Status Panel")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted Today", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 AI Suggestion Feed")
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
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚖️ Human vs AI Effectiveness")
    effect_data = pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    })
    st.dataframe(effect_data, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📈 Behavior-Based Segmentation")
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(segment_data, names="Segment", values="Count", hole=0.4, 
                         color_discrete_sequence=flowen_colors)
    st.plotly_chart(fig_segment, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Loan Type Breakdown")
    loan_dist = df["loan_type"].value_counts().reset_index()
    loan_dist.columns = ["Loan Type", "Count"]
    fig_loan = px.pie(
        loan_dist,
        names="Loan Type",
        values="Count",
        hole=0.4,
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_loan, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📉 Average DPD by Age Group")
    df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(
        age_dpd,
        x="age_group",
        y="dpd",
        color="age_group",
        color_discrete_sequence=flowen_colors,
        title="Avg Days Past Due by Age Group"
    )
    st.plotly_chart(fig_age, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Debtor Summary")
    selected_name = st.selectbox("🔍 Click a debtor to view profile", df["name"].unique())
    filtered = df[df["name"] == selected_name].iloc[0]
    st.markdown(f"""
        **Account ID:** {filtered['account_id']}  
        **Risk Score:** {filtered['risk_score']} | **Risk Level:** {filtered['risk_level']}  
        **Outstanding:** ฿{filtered['total_debt']:,} | **DPD:** {filtered['dpd']}  
        **Loan Type:** {filtered['loan_type']} | **Region:** {filtered['region']}  
        **Contact Channel:** {filtered['contact_channel']} | **Last Payment:** {filtered['last_payment_date']}
    """)
    st.markdown("</div>", unsafe_allow_html=True)
