import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# ─── Configuration ─────────────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── Logo Top Left ─────────────────────────
st.markdown("""
    <style>
        .flowen-logo {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 100;
        }
    </style>
    <div class="flowen-logo">
        <img src="data:image/png;base64,{}" width="120"/>
    </div>
""".format(base64.b64encode(open("flowen_logo.png", "rb").read()).decode()), unsafe_allow_html=True)


# ─── Custom Theme Styling ──────────────────────────────────────
st.markdown("""
    <style>
        body {
            background-color: #F9FAFB;
        }
        .main > div {
            padding: 2rem;
        }
        .css-1d391kg, .css-1kyxreq {
            background-color: #0A2342 !important;
            color: white !important;
        }
        .block-container {
            padding-top: 0rem;
        }
        .stCard {
            background-color: white;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ─── Load Assets ────────────────────────────────────────────────
logo = Image.open("flowen_logo.png")

# ─── Header: Logo & Language Toggle ─────────────────────────────
colA, colB = st.columns([6, 1])
with colA:
    st.image(logo, width=160)
with colB:
    lang = st.selectbox("🌐 Language", options=["🇬🇧 English", "🇹🇭 ภาษาไทย"], key="lang_toggle")

# ─── Load Data ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── Sidebar Navigation ─────────────────────────────────────────
menu = st.sidebar.radio("📊 Menu", ["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])
st.sidebar.markdown("")

# ─── Custom Plotly Theme ────────────────────────────────────────
plotly_colors = ['#00B88C', '#0072B5', '#A2D729', '#42C2FF', '#008C76']

# ─── RISK OVERVIEW ──────────────────────────────────────────────
if menu == "Risk Overview":
    st.markdown("## Risk Overview")

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📞 Contacted Today", "1,203")
        col2.metric("📬 Responses", "645")
        col3.metric("💬 Conversations", "53")
        col4.metric("✅ Paid <24h", "32%")

    with st.container():
        st.markdown("#### 🎯 AI Suggestion")
        st.dataframe(
            df.sort_values("ai_risk_score", ascending=False)
            .head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]],
            use_container_width=True
        )

    with st.container():
        st.markdown("#### 📉 Risk Segments")
        segment_data = df["response_behavior"].value_counts().reset_index()
        segment_data.columns = ["Segment", "Count"]
        fig_segment = px.pie(segment_data, names="Segment", values="Count", hole=0.4)
        fig_segment.update_traces(marker=dict(colors=plotly_colors))
        st.plotly_chart(fig_segment, use_container_width=True)

    with st.container():
        st.markdown("#### 📊 Loan Type Breakdown")
        loan_dist = df["loan_type"].value_counts().reset_index()
        loan_dist.columns = ["Loan Type", "Count"]
        fig_loan = px.pie(loan_dist, names="Loan Type", values="Count", hole=0.4)
        fig_loan.update_traces(marker=dict(colors=plotly_colors))
        st.plotly_chart(fig_loan, use_container_width=True)

    with st.container():
        st.markdown("#### 🧓 DPD by Age Group")
        df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
        age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
        fig_age = px.bar(age_dpd, x="age_group", y="dpd", color="age_group", color_discrete_sequence=plotly_colors)
        fig_age.update_layout(xaxis_title="Age Group", yaxis_title="Avg DPD")
        st.plotly_chart(fig_age, use_container_width=True)

    with st.container():
        st.markdown("#### 🧾 Debtor Table (clickable)")
        selected_name = st.selectbox("🔎 Select debtor", df["name"].unique())
        selected_row = df[df["name"] == selected_name].iloc[0]
        st.markdown(f"**Name:** {selected_row['name']}  \n**ID:** {selected_row['account_id']}")
        st.markdown(f"**Risk Score:** {selected_row['risk_score']} | **Risk Level:** {selected_row['risk_level']}")
        st.markdown(f"**Outstanding:** ฿{selected_row['total_debt']:,} | **DPD:** {selected_row['dpd']} days")
        st.markdown(f"**Loan Type:** {selected_row['loan_type']} | **Region:** {selected_row['region']}")
        st.markdown(f"**Contact:** {selected_row['contact_channel']} | **Last Payment:** {selected_row['last_payment_date']}")

# ─── OTHER PAGES ────────────────────────────────────────────────
# (กรุณาให้ฉันดำเนินการต่อเพื่อเขียน `Journey Management`, `Recovery KPI`, `Behavioral Insights` 
# ตามสไตล์เดียวกันนี้)

