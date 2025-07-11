# flowen_dashboard_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── Load Flowen Logo from base64 ─────────────────────────────────────────────
logo_base64 = """<Flowen_logo>"""

html_top = """
<div style="display: flex; justify-content: space-between; align-items: center;">
    <img src="data:image/png;base64,{logo}" width="140" style="margin-bottom:10px;" />
    <select onchange="window.location.search='lang='+this.value" style="padding:5px;border-radius:5px;">
        <option value=\"en\">&#127468;&#127463; EN</option>
        <option value=\"th\">&#127481;&#127469; TH</option>
    </select>
</div>
<hr style=\"margin-top:10px; margin-bottom:20px;\">
""".format(logo=logo_base64)

st.markdown(html_top, unsafe_allow_html=True)

# ─── Global Style ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="column"] > div {
    border: 1px solid #E0E0E0;
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    background-color: #ffffff;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─── Realtime Notification Mock ───────────────────────────────────────────────
st.markdown("""
<div style="background-color:#e8f9f0;border-left:6px solid #0aaf8d;padding:10px 20px;margin-bottom:20px;">
  🔔 <strong>Realtime Alert:</strong> 3 accounts exceeded 45+ DPD today. <a href="#">[View Now]</a>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── Color Theme ──────────────────────────────────────────────────────────────
FLOWEN_COLORS = ["#0aaf8d", "#28c7fa", "#005f73"]

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
menu = st.sidebar.radio("Navigation", [
    "Risk Overview",
    "Journey Management",
    "Recovery KPI",
    "Behavioral Insights"
])

# ─── Placeholder for each page ────────────────────────────────────────────────
if menu == "Risk Overview":
    st.title("🔎 Risk Overview")

    # ─── Summary Metrics ───────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted Today", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")

    # ─── AI Suggestions ─────────────────────────────
    st.subheader("Top 5 Accounts Likely to Pay in 48h")
    top5 = df.sort_values("ai_risk_score", ascending=False).head(5)
    st.table(top5[["account_id", "name", "risk_score", "loan_type", "contact_channel"]])

    # ─── Inactive Accounts ───────────────────────────
    st.subheader("Accounts Ignored All Contact for 30+ Days")
    inactive = df[df["last_payment_days_ago"] > 30].sort_values("risk_score", ascending=False)
    st.dataframe(
        inactive[["account_id", "name", "risk_score", "last_payment_days_ago", "region"]],
        use_container_width=True
    )

    # ─── Human vs AI Comparison ─────────────────────
    st.subheader("⚖️ Human vs AI Effectiveness")
    effect_data = pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    })
    st.dataframe(effect_data)

    # ─── AI Learning System ──────────────────────────
    st.subheader("AI Self-Learning System")
    st.info("AI last retrained: **2 hours ago**  
Top new feature: **Contact Channel**  
Next model update in: **22 hours**")

    # ─── Debtor Segmentation ─────────────────────────
    st.subheader("Debtor Segment Overview")
    seg_data = df["response_behavior"].value_counts().reset_index()
    seg_data.columns = ["Segment", "Count"]
    fig_segment = px.pie(seg_data, names="Segment", values="Count", hole=0.4, title="Behavior Segmentation",
                         color_discrete_sequence=FLOWEN_COLORS)
    st.plotly_chart(fig_segment, use_container_width=True)

    # ─── Loan Type Distribution ──────────────────────
    st.subheader("Loan Type Breakdown")
    loan_data = df["loan_type"].value_counts().reset_index()
    loan_data.columns = ["Loan Type", "Count"]
    fig_loan = px.pie(loan_data, names="Loan Type", values="Count", hole=0.4,
                      color_discrete_sequence=FLOWEN_COLORS)
    st.plotly_chart(fig_loan, use_container_width=True)

    # ─── Payment Delay by Age Group ─────────────────
    st.subheader("Avg Days Past Due by Age Group")
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(age_dpd, x="age_group", y="dpd",
                     labels={"dpd": "Avg DPD", "age_group": "Age Group"},
                     color="age_group", color_discrete_sequence=FLOWEN_COLORS)
    st.plotly_chart(fig_age, use_container_width=True)

    # ─── Debtor Summary Table ───────────────────────
    st.subheader("Debtor Summary")
    st.dataframe(df[[
        "account_id", "name", "risk_score", "total_debt", "dpd", "loan_type", "region", "risk_level"]],
        use_container_width=True)

    # ─── Debtor Profile View ────────────────────────
    st.subheader("Debtor Profile Viewer")
    selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
    debtor = df[df["account_id"] == selected_account].iloc[0]
    st.markdown(f"**Name:** {debtor['name']}  ")
    st.markdown(f"**Risk Score:** {debtor['risk_score']} | Risk Level: {debtor['risk_level']}")
    st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | DPD: {debtor['dpd']} days")
    st.markdown(f"**Loan Type:** {debtor['loan_type']} | Region: {debtor['region']}")
    st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | Last Payment: {debtor['last_payment_date']}")

elif menu == "Journey Management":
    st.title("Journey Management")
    # You can place Journey content here...

elif menu == "Recovery KPI":
    st.title("Recovery KPI")
    # You can place KPI content here...

elif menu == "Behavioral Insights":
    st.title("Behavioral Insights")
    # You can place Behavioral Insights content here...

