import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# ─── Set Flowen CI Colors ─────────────────────
flowen_colors = ["#00B894", "#0984E3", "#FDCB6E", "#6C5CE7", "#00CEC9"]

# ─── Encode Flowen Logo ───────────────────────
def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# ─── Inject Flowen Theme ──────────────────────
st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{
        background-color: #0a2342;
    }}
    .lang-toggle {{
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 1000;
    }}
</style>
<div style="position:fixed; top:10px; left:10px; z-index:1000;">
    <img src="data:image/png;base64,{logo_base64}" width="140"/>
</div>
""", unsafe_allow_html=True)

# ─── Page Config ──────────────────────────────
st.set_page_config(layout="wide")
st.title("Flowen: Debt Collection AI Dashboard")

# ─── Load Data ────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── Sidebar ──────────────────────────────────
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=150)
menu = st.sidebar.radio("Navigation", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# --- Risk Overview ---
if menu == "Risk Overview":
    st.title(" Risk Overview")

    st.markdown("###  Real-Time Status Panel")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Accounts Contacted Today", "1,203")
    col2.metric(" Responses Received", "645")
    col3.metric(" Active Conversations", "53")
    col4.metric(" Paid Within 24h", "32%")

    st.markdown("###  AI Suggestion Feed")
    with st.expander("Top 5 Accounts Likely to Pay in 48h"):
        st.table(df.sort_values("ai_risk_score", ascending=False).head(5)[[
            "account_id", "name", "risk_score", "loan_type", "contact_channel"
        ]].rename(columns={
            "account_id": "Account ID", "name": "Name", "risk_score": "Risk Score",
            "loan_type": "Loan Type", "contact_channel": "Contact Channel"
        }))

    with st.expander("Accounts Ignored All Contact for 7+ Days"):
        inactive = df[df["last_payment_days_ago"] > 30].sort_values("risk_score", ascending=False)
        st.dataframe(inactive[[
            "account_id", "name", "risk_score", "last_payment_days_ago", "region"
        ]].rename(columns={
            "account_id": "Account ID", "name": "Name", "risk_score": "Risk Score",
            "last_payment_days_ago": "Last Payment (Days Ago)", "region": "Region"
        }).head(5), use_container_width=True)

    st.markdown("### ⚖️ Human vs AI Effectiveness")
    effect_data = pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    })
    st.dataframe(effect_data)

    st.markdown("###  AI Self-Learning System")
    st.info("AI last retrained: **2 hours ago**  \nTop new feature: **Contact Channel**  \nNext model update in: **22 hours**")

    st.markdown("###  Debtor Segment Overview")
    segment_data = df["response_behavior"].value_counts().reset_index()
    segment_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(segment_data, names="Segment", values="Count", hole=0.4, title="Behavior-Based Segmentation", color_discrete_sequence=flowen_colors)
    st.plotly_chart(fig_segment, use_container_width=True)

    st.markdown("###  Loan Type Distribution")
    loan_dist = df["loan_type"].value_counts().reset_index()
    loan_dist.columns = ["Loan Type", "Count"]
    fig_loan = px.pie(loan_dist, names="Loan Type", values="Count", title="Loan Type Breakdown", hole=0.4, color_discrete_sequence=flowen_colors)
    st.plotly_chart(fig_loan, use_container_width=True)

    st.markdown("###  Payment Delay by Age Group")
    df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(age_dpd, x="age_group", y="dpd", title="Average Days Past Due by Age Group", labels={"dpd": "Avg DPD", "age_group": "Age Group"}, color_discrete_sequence=flowen_colors)
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("###  Debtor Summary")
    st.dataframe(df[[
        "account_id", "name", "risk_score", "total_debt", "dpd",
        "loan_type", "region", "risk_level"
    ]].rename(columns={
        "account_id": "Account ID", "name": "Name", "risk_score": "Risk Score",
        "total_debt": "Outstanding (฿)", "dpd": "Days Past Due",
        "loan_type": "Loan Type", "region": "Region", "risk_level": "Risk Level"
    }), use_container_width=True)

    st.markdown("###  Debtor Profile Viewer")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")
