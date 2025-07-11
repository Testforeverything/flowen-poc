import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── PAGE CONFIG ───────────────────────────────────────
st.set_page_config(page_title="Flowen Dashboard", layout="wide")

# ─── CSS THEME ─────────────────────────────────────────
st.markdown("""
    <style>
        .main { background-color: #F7FAFC; }
        [data-testid="stSidebar"] {
            background-color: #0A2342;
        }
        [data-testid="stSidebar"] * {
            color: #FFFFFF;
            font-size: 16px;
        }
        h1, h2, h3, h4 {
            color: #0A2342;
        }
        div[data-testid="metric-container"] {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 5px;
        }
        [data-testid="stExpander"] {
            background-color: #f0f4f8;
            border: 1px solid #dce3eb;
        }
        .stButton > button {
            background-color: #2CA8D2;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ─────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── SIDEBAR ───────────────────────────────────────────
st.sidebar.image("https://i.imgur.com/UOa1y7O.png", width=160)
lang = st.sidebar.selectbox("🌐 Language", ["🇬🇧 EN", "🇹🇭 TH"])
menu = st.sidebar.radio("["Risk Overview", "Journey Management", "Recovery KPI", "Behavioral Insights"])

# ─── COLOR THEME ───────────────────────────────────────
brand_colors = ["#2CA8D2", "#21B573", "#0A2342"]

# ─── PAGE: RISK OVERVIEW ───────────────────────────────
if menu == "Risk Overview":
    title = "Risk Overview" if lang == "🇬🇧 EN" else "ภาพรวมความเสี่ยง"
    st.title(f"📌 {title}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Accounts Contacted Today", "1,203")
    col2.metric("Responses Received", "645")
    col3.metric("Active Conversations", "53")
    col4.metric("Paid Within 24h", "32%")

    st.subheader("🔍 AI Suggestion Feed")
    with st.expander("Top 5 Accounts Likely to Pay in 48h"):
        st.table(df.sort_values("ai_risk_score", ascending=False).head(5)[["account_id", "name", "risk_score", "loan_type", "contact_channel"]])

    with st.expander("Accounts Ignored All Contact for 7+ Days"):
        st.dataframe(
            df[df["last_payment_days_ago"] > 30]
            .sort_values("risk_score", ascending=False)
            .head(5)[["account_id", "name", "risk_score", "last_payment_days_ago", "region"]],
            use_container_width=True
        )

    st.subheader(" Human vs AI Effectiveness")
    st.dataframe(pd.DataFrame({
        "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
        "Success Rate (%)": [72, 51, 43],
        "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
    }))

    st.info(" AI last retrained: 2 hours ago | Top new feature: Contact Channel | Next model update in: 22 hours")

    st.subheader(" Behavior-Based Segmentation")
    segment_data = df["response_behavior"].value_counts().reset_index()
    fig_segment = px.pie(segment_data, names="index", values="response_behavior", hole=0.4,
                         color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_segment, use_container_width=True)

    st.subheader(" Loan Type Breakdown")
    loan_dist = df["loan_type"].value_counts().reset_index()
    fig_loan = px.pie(loan_dist, names="index", values="loan_type", hole=0.4,
                      color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_loan, use_container_width=True)

    st.subheader(" Avg DPD by Age Group")
    df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
    age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
    fig_age = px.bar(age_dpd, x="age_group", y="dpd", labels={"dpd": "Avg DPD"},
                     color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_age, use_container_width=True)

    st.subheader(" Debtor Summary (Click to View)")
    selected_name = st.selectbox("🔍 Select Debtor", df["name"].unique())
    selected_debtor = df[df["name"] == selected_name].iloc[0]

    with st.expander(f" Debtor Profile: {selected_name}"):
        st.write(f"**Account ID:** {selected_debtor['account_id']}")
        st.write(f"**Risk Score:** {selected_debtor['risk_score']} | Risk Level: {selected_debtor['risk_level']}")
        st.write(f"**Outstanding:** ฿{selected_debtor['total_debt']:,} | DPD: {selected_debtor['dpd']} days")
        st.write(f"**Loan Type:** {selected_debtor['loan_type']} | Region: {selected_debtor['region']}")
        st.write(f"**Contact Channel:** {selected_debtor['contact_channel']}")
        st.write(f"**Last Payment:** {selected_debtor['last_payment_date']}")

# ─── PAGE: JOURNEY MANAGEMENT ──────────────────────────
elif menu == "Journey Management":
    title = "Journey Management" if lang == "🇬🇧 EN" else "จัดการการเดินทางลูกหนี้"
    st.title(f"🚀 {title}")

    st.subheader(" Journey Funnel")
    funnel_data = pd.DataFrame({
        "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
        "Count": [8500, 5200, 2100, 865]
    })
    fig_funnel = px.funnel(funnel_data, x="Count", y="Stage", color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.subheader(" Journey Performance")
    journey_perf = pd.DataFrame({
        "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Prompt", "Manual Call"],
        "Conversion Rate (%)": [31, 42, 38, 28],
        "Avg Days to Pay": [4.2, 3.5, 4.0, 6.1]
    })
    st.dataframe(journey_perf)

# ─── PAGE: RECOVERY KPI ───────────────────────────────
elif menu == "Recovery KPI":
    title = "Recovery KPI" if lang == "🇬🇧 EN" else "ดัชนีการเก็บหนี้"
    st.title(f" {title}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Recovered", "฿12,850,000")
    col2.metric("Recovery Rate", "64.7%")
    col3.metric("Avg. Time to Recovery", "3.6 days")
    col4.metric("Active Collectors", "12")

    st.subheader(" Daily Recovery Trend")
    trend_data = pd.DataFrame({
        "Date": pd.date_range("2025-07-01", periods=10, freq="D"),
        "Recovered": [1000000, 1250000, 1380000, 1220000, 1500000, 1600000, 1700000, 1450000, 1550000, 1650000]
    })
    fig_trend = px.line(trend_data, x="Date", y="Recovered", markers=True, color_discrete_sequence=[brand_colors[0]])
    st.plotly_chart(fig_trend, use_container_width=True)

# ─── PAGE: BEHAVIORAL INSIGHTS ────────────────────────
elif menu == "Behavioral Insights":
    title = "Behavioral Insights" if lang == "🇬🇧 EN" else "พฤติกรรมลูกหนี้"
    st.title(f" {title}")

    st.subheader(" Response Behavior")
    response_counts = df["response_behavior"].value_counts().reset_index()
    fig_response = px.pie(response_counts, names="index", values="response_behavior", hole=0.4,
                          color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_response, use_container_width=True)

    st.subheader(" Monthly Income Distribution")
    fig_income = px.histogram(df, x="monthly_income", nbins=30, color_discrete_sequence=[brand_colors[1]])
    st.plotly_chart(fig_income, use_container_width=True)

    st.subheader(" Channel vs Behavior")
    chan_beh = df.groupby(["contact_channel", "response_behavior"]).size().reset_index(name="Count")
    fig_chan = px.bar(chan_beh, x="contact_channel", y="Count", color="response_behavior",
                      barmode="group", color_discrete_sequence=brand_colors)
    st.plotly_chart(fig_chan, use_container_width=True)
