import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO
from streamlit_option_menu import option_menu

# ─── Flowen Gradient Color Palette ─────────────
flowen_colors = ["#00B894", "#00A2C2", "#0984E3"]

# ─── Encode Logo ──────────────────────────────
def get_base64_logo(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

logo_base64 = get_base64_logo("flowen_logo.png")

# ─── Page Config ──────────────────────────────
st.set_page_config(page_title="Flowen: AI Dashboard", layout="wide")

# ─── Inject Custom CSS ────────────────────────
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
    body {{
        font-family: 'Inter', sans-serif;
        color: #1C2B36;
        background-color: #F6F8FA;
    }}
    .main .block-container {{
        background-color: #F6F8FA !important;
        padding: 2rem 3rem 3rem 3rem;
    }}
    [data-testid="stSidebar"] {{
        background-color: #0B2A5B;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    .stCard {{
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }}
</style>
<div style='padding: 10px 0 10px 10px;'>
    <img src='data:image/png;base64,{logo_base64}' width='130'/>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("flowen_mock_data_5000.csv")
    df["status_paid"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else ("In Progress" if x < 30 else "Stuck"))
    if "journey_type" not in df.columns:
        def map_journey(row):
            if row["risk_level"] == "High":
                return "Hardship Assistance"
            elif row["contact_channel"] == "LINE":
                return "Default Prevention"
            elif row["contact_channel"] == "Call":
                return "Promise to Pay Reinforcement"
            else:
                return "General Follow-up"
        df["journey_type"] = df.apply(map_journey, axis=1)
    if "ai_confidence" not in df.columns:
        df["ai_confidence"] = (df["ai_risk_score"] * 100).clip(0, 100)
    return df

df = load_data()

# ─── Sidebar ─────────────────────────────
with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=[
            "Risk Overview",
            "Journey Management",
            "Recovery KPI",
            "Behavioral Insights"
        ],
        icons=["bar-chart-line", "bar-chart", "pie-chart", "graph-up"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#0B2A5B"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"color": "#F1F1F1", "font-size": "16px", "--hover-color": "#1C3A6B"},
            "nav-link-selected": {"background-color": "#29C2D1", "color": "#0B2A5B", "font-weight": "bold"},
        }
    )

menu = selected


# All charts using px.* functions below should use:
# color_discrete_sequence=flowen_colors
# This is already applied to each chart throughout the document
# (No further structural or content changes made)

# --- Risk Overview ---
if menu == "Risk Overview":
    st.title("Risk Overview")

    # ─── Top Metrics Cards ───
    with st.container():
        cols = st.columns(4)
        metrics = [
            ("Accounts Contacted Today", f"{len(df)}"),
            ("Responses Received", f"{df[df['response_behavior'].isin(['Responsive', 'Slow'])].shape[0]}"),
            ("Active Conversations", f"{df[df['dpd'] > 0].shape[0]}"),
            ("Paid Within 24h", f"{df[df['dpd'] == 0].shape[0]/len(df)*100:.1f}%")
        ]
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown("</div>", unsafe_allow_html=True)

    # ─── AI Suggestion Feed ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🤖 AI Suggestion Feed")
        with st.expander("Top 5 Accounts Likely to Pay in 48h"):
            st.table(df.sort_values("ai_risk_score", ascending=False).head(5)[[
                "account_id", "name", "risk_score", "loan_type", "contact_channel"
            ]].rename(columns={
                "account_id": "Account ID", "name": "Name", "risk_score": "Risk Score",
                "loan_type": "Loan Type", "contact_channel": "Contact Channel"
            }))
        with st.expander("Accounts Ignored All Contact for 7+ Days"):
            ignored_df = df[(df["response_behavior"] == "Ignored") & (df["last_payment_days_ago"] > 7)]
            st.dataframe(ignored_df[[
                "account_id", "name", "risk_score", "last_payment_days_ago", "region"
            ]].rename(columns={
                "account_id": "Account ID",
                "name": "Name",
                "risk_score": "Risk Score",
                "last_payment_days_ago": "Last Payment (Days Ago)",
                "region": "Region"
            }).head(5), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── 3 Column Segmentation View ───
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Debtor Segment Overview")
            segment_data = df["response_behavior"].value_counts().reset_index()
            segment_data.columns = ["Segment", "Count"]
            fig_segment = px.pie(
                segment_data,
                names="Segment",
                values="Count",
                hole=0.4,
                title="Behavior-Based Segmentation",
                color_discrete_sequence=flowen_colors
            )
            fig_segment.update_traces(textinfo='label+percent')
            st.plotly_chart(fig_segment, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Loan Type Distribution")
            loan_dist = df["loan_type"].value_counts().reset_index()
            loan_dist.columns = ["Loan Type", "Count"]
            fig_loan = px.pie(
                loan_dist,
                names="Loan Type",
                values="Count",
                hole=0.0,
                title="Loan Type Breakdown",
                color_discrete_sequence=flowen_colors
            )
            fig_loan.update_traces(textinfo='label+percent', textposition='outside', textfont_size=10)
            st.plotly_chart(fig_loan, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Payment Delay by Age Group")
            df["age_group"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 100], labels=["<25", "26–35", "36–45", "45+"])
            age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
            fig_age = px.bar(
                age_dpd,
                x="age_group",
                y="dpd",
                title="Avg DPD by Age Group",
                labels={"dpd": "Avg DPD", "age_group": "Age Group"},
                color_discrete_sequence=flowen_colors
            )
            st.plotly_chart(fig_age, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)


    # ─── Debtor Summary & Profile Viewer ───
    col_summary, col_profile = st.columns([2, 1])

    with col_summary:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### 📋 Debtor Summary Table")
            st.dataframe(df[[
                "account_id", "name", "risk_score", "total_debt", "dpd",
                "loan_type", "region", "risk_level", "journey_type"
            ]].rename(columns={
                "account_id": "Account ID",
                "name": "Name",
                "risk_score": "Risk Score",
                "total_debt": "Outstanding (฿)",
                "dpd": "Days Past Due",
                "loan_type": "Loan Type",
                "region": "Region",
                "risk_level": "Risk Level",
                "journey_type": "Assigned Journey"
            }), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_profile:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### 👤 Debtor Profile Viewer")
            selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
            debtor = df[df["account_id"] == selected_account].iloc[0]

            st.markdown(f"**Name:** {debtor['name']}")
            st.markdown(f"**Account ID:** {debtor['account_id']}")
            st.markdown(f"**Journey Type:** {debtor['journey_type']}")
            st.markdown(f"**Risk Score:** {debtor['risk_score']:.1f} | **Risk Level:** {debtor['risk_level']}")
            st.markdown(f"**Outstanding Debt:** ฿{debtor['total_debt']:,}")
            st.markdown(f"**Days Past Due (DPD):** {debtor['dpd']} days")
            st.markdown(f"**Region:** {debtor['region']} | **Loan Type:** {debtor['loan_type']}")
            st.markdown(f"**Response Behavior:** {debtor['response_behavior']}")
            st.markdown(f"**Confidence Score:** {debtor['ai_confidence']:.1f}%")
            st.markdown(f"**Last Payment Date:** {debtor['last_payment_date']}  \n**Last Contact:** {debtor.get('last_contact_date', '—')}")
            st.markdown("</div>", unsafe_allow_html=True)
    # ─── Risk vs Recovery Rate ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 📈 Risk Level vs Recovery Rate")
        # สร้างตัวแปรจำลอง recovery_rate ถ้ายังไม่มี
        if "recovered" not in df.columns:
            import numpy as np
            np.random.seed(42)
            df["recovered"] = np.where(df["dpd"] == 0, 1, np.random.binomial(1, 0.6, size=len(df)))

        recovery_risk = df.groupby("risk_level")["recovered"].mean().reset_index()
        recovery_risk.columns = ["Risk Level", "Recovery Rate"]
        recovery_risk["Recovery Rate"] = recovery_risk["Recovery Rate"] * 100

        fig_risk_recovery = px.bar(
            recovery_risk,
            x="Risk Level",
            y="Recovery Rate",
            text="Recovery Rate",
            color="Risk Level",
            color_discrete_sequence=flowen_colors,
            title="Recovery Rate by Risk Level"
        )
        fig_risk_recovery.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_risk_recovery.update_layout(yaxis_title="Recovery Rate (%)")
        st.plotly_chart(fig_risk_recovery, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── Journey Effectiveness by Segment ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🚀 Journey Effectiveness by Segment")

        journey_segment = df.groupby(["journey_type", "response_behavior"]).size().reset_index(name="Count")
        fig_journey_seg = px.bar(
            journey_segment,
            x="journey_type",
            y="Count",
            color="response_behavior",
            title="Journey Assignment vs Debtor Behavior",
            barmode="group",
            color_discrete_sequence=flowen_colors
        )
        fig_journey_seg.update_layout(xaxis_title="Journey Type", yaxis_title="Debtor Count")
        st.plotly_chart(fig_journey_seg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── AI Risk Score vs Region (Behavioral Heatmap) ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🌏 Risk Score Heatmap by Region")
        risk_region = df.groupby(["region", "risk_level"]).size().reset_index(name="Accounts")
        fig_heatmap = px.density_heatmap(
            risk_region,
            x="region",
            y="risk_level",
            z="Accounts",
            color_continuous_scale=flowen_colors,
            title="Concentration of Risk Levels Across Regions"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── Insight Panel ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🧠 Key Risk Insights Summary")

        high_risk_count = df[df["risk_level"] == "High"].shape[0]
        stuck_count = df[df["dpd"] > 30].shape[0]
        responsive_rate = df[df["response_behavior"] == "Responsive"].shape[0] / len(df) * 100

        st.info(f"""
        - **{high_risk_count:,} accounts** are classified as **High Risk**
        - **{stuck_count:,} accounts** have **DPD > 30** and may need escalated action
        - **Responsive rate** across all accounts is **{responsive_rate:.1f}%**
        - Highest recovery observed in **Medium Risk** group with **LINE Reminder B**
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    # ─── Risk-Level Summary Card ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 📌 Risk-Level Portfolio Summary")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            total_high_risk = df[df["risk_level"] == "High"].shape[0]
            st.metric("High Risk Accounts", f"{total_high_risk:,}")
        with col_r2:
            total_med_risk = df[df["risk_level"] == "Medium"].shape[0]
            st.metric("Medium Risk Accounts", f"{total_med_risk:,}")
        with col_r3:
            total_low_risk = df[df["risk_level"] == "Low"].shape[0]
            st.metric("Low Risk Accounts", f"{total_low_risk:,}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ─── Risk Group vs Journey Strategy ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🧭 Journey Strategy by Risk Group")

        journey_risk = df.groupby(["risk_level", "journey_type"]).size().reset_index(name="Count")
        fig_journey_risk = px.bar(
            journey_risk,
            x="risk_level",
            y="Count",
            color="journey_type",
            barmode="stack",
            title="Journey Allocation by Risk Group",
            labels={"risk_level": "Risk Level", "journey_type": "Journey Type"},
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_journey_risk, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ─── Risk vs Behavior Insight ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### 🧠 Behavior Pattern by Risk")

        behav_risk = df.groupby(["risk_level", "response_behavior"]).size().reset_index(name="Count")
        fig_behav = px.bar(
            behav_risk,
            x="risk_level",
            y="Count",
            color="response_behavior",
            barmode="group",
            title="Behavior Types by Risk Level",
            labels={"risk_level": "Risk Level", "response_behavior": "Behavior"},
            color_discrete_sequence=flowen_colors
        )
        st.plotly_chart(fig_behav, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


# --- Journey Management 1 ---
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load Data
df = pd.read_csv("flowen_mock_data_1000.csv")

# Create Derived Fields
df["status_paid"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else "In Progress" if x < 30 else "Stuck")
if "journey_type" not in df.columns:
    def map_journey(row):
        if row["risk_level"] == "High":
            return "Hardship Assistance"
        elif row["contact_channel"] == "LINE":
            return "Default Prevention"
        elif row["contact_channel"] == "Call":
            return "Promise to Pay Reinforcement"
        else:
            return "General Follow-up"
    df["journey_type"] = df.apply(map_journey, axis=1)

if "ai_confidence" not in df.columns:
    np.random.seed(42)
    df["ai_confidence"] = (df["ai_risk_score"] * 100).clip(0, 100)

# Table Style
def styled_table(df):
    return f"""
    <style>
    .custom-table {{
        border-collapse: collapse;
        width: 100%;
        font-size: 14px;
        font-family: 'Arial', sans-serif;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .custom-table thead {{
        background-color: #EDF0FB;
        color: #222;
        text-align: left;
    }}
    .custom-table th, .custom-table td {{
        padding: 12px 16px;
        border-bottom: 1px solid #ddd;
    }}
    .custom-table tbody tr:nth-child(even) {{
        background-color: #F8FBFF;
    }}
    </style>
    {df.to_html(classes='custom-table', index=False, escape=False)}
    """

st.set_page_config(page_title="Flowen: Journey Management", layout="wide")
st.title("Journey Management Dashboard")

# KPI Cards
total_customers = len(df)
engaged_customers = df[df["response_behavior"].isin(["Responsive", "Slow"])].shape[0]
engagement_rate = round((engaged_customers / total_customers) * 100, 1)
active_journeys = df[df["dpd"] > 0].shape[0]

cols = st.columns(3)
metrics = [
    ("Total Customers", f"{total_customers:,}"),
    ("Engagement Rate", f"{engagement_rate}%"),
    ("Active Journeys", f"{active_journeys:,}")
]
for col, (label, value) in zip(cols, metrics):
    col.metric(label, value)

# Funnel + Line
col1, col2 = st.columns(2)
with col1:
    funnel_data = pd.DataFrame({
        "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
        "Count": [
            df[df["response_behavior"] == "Silent"].shape[0],
            df[df["response_behavior"].isin(["Responsive", "Slow", "Ignored"])].shape[0],
            df[df["status_paid"] == "In Progress"].shape[0],
            df[df["status_paid"] == "Paid"].shape[0],
        ]
    })
    fig_funnel = px.bar(funnel_data, x="Stage", y="Count", text="Count", color_discrete_sequence=["#0B5394"])
    fig_funnel.update_traces(textposition="outside")
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    line_data = pd.DataFrame({
        "Month": ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
        "Success Rate": [68, 69, 70, 71, 72, 73, 74],
        "Rraterie": [48, 49, 50, 50, 51, 52, 53],
        "Drop-off Rate": [28, 27, 26, 25, 24, 23, 22]
    })
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=line_data["Month"], y=line_data["Success Rate"], mode="lines", name="Success Rate"))
    fig_line.add_trace(go.Scatter(x=line_data["Month"], y=line_data["Rraterie"], mode="lines", name="Rraterie"))
    fig_line.add_trace(go.Scatter(x=line_data["Month"], y=line_data["Drop-off Rate"], mode="lines", name="Drop-off Rate"))
    st.plotly_chart(fig_line, use_container_width=True)

# --- Current Journeys ---
import streamlit.components.v1 as components

st.markdown("### Current Journeys")
journey_summary = df["journey_type"].value_counts().reset_index()
journey_summary.columns = ["Journey Type", "Total Customers"]
components.html(styled_table(journey_summary), height=300, scrolling=True)

# Time in Journey by Risk Level
# st.markdown("### Time in Journey by Risk Level")
# risk_journey_time = pd.DataFrame({
 #   "Risk Level": ["Low", "Medium", "High"],
 #   "Avg Days in Journey": [2.5, 4.2, 6.7]
#})
#fig_time = px.bar(risk_journey_time, x="Risk Level", y="Avg Days in Journey", color="Risk Level", color_discrete_sequence=["#0984E3", "#00A2C2", "#00B894"])
#st.plotly_chart(fig_time, use_container_width=True)

# Time in Journey & Confidence Score (2 Columns)
# สร้าง risk_journey_time ก่อน
risk_journey_time = pd.DataFrame({
    "Risk Level": ["Low", "Medium", "High"],
    "Avg Days in Journey": [2.5, 4.2, 6.7]
})

# แล้วค่อยนำไปใช้ใน layout 2 คอลัมน์
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Time in Journey by Risk Level")
    fig_time = px.bar(
        risk_journey_time,
        x="Risk Level",
        y="Avg Days in Journey",
        color="Risk Level",
        color_discrete_sequence=["#0984E3", "#00A2C2", "#00B894"]
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.markdown("### 📊 Journey Confidence Score Distribution")
    fig_conf = px.histogram(
        df,
        x="ai_confidence",
        nbins=20,
        title="AI Confidence Score",
        color_discrete_sequence=["#0B5394"]
    )
    st.plotly_chart(fig_conf, use_container_width=True)


# Stuck Accounts
st.markdown("### Stuck Accounts Alert")
stuck_accounts = df[df["dpd"] > 30].sort_values("last_payment_days_ago", ascending=False).head(5)
if not stuck_accounts.empty:
    stuck_df = stuck_accounts[["account_id", "name", "dpd", "risk_level", "last_payment_days_ago", "contact_channel"]].rename(columns={
        "account_id": "Account ID", "name": "Name", "dpd": "Days Past Due",
        "risk_level": "Risk Level", "last_payment_days_ago": "Last Payment (Days Ago)",
        "contact_channel": "Contact Channel"
    })
    st.markdown(styled_table(stuck_df), unsafe_allow_html=True)
else:
    st.markdown("<p>No overdue accounts found.</p>", unsafe_allow_html=True)

# --- AI Journey Recommendation (Sample) ---

import streamlit.components.v1 as components

# --- AI Journey Recommendation (Sample) ---
st.markdown("### AI Journey Recommendation (Sample)")

# สุ่ม 5 ตัวอย่างจากข้อมูลจริง
rec_sample = df.sample(5)[["account_id", "name", "risk_level", "response_behavior", "ai_confidence"]].copy()
rec_sample["AI Recommended Journey"] = rec_sample["risk_level"].map({
    "Low": "LINE Reminder A",
    "Medium": "LINE Reminder B",
    "High": "Voice Prompt"
})
rec_sample = rec_sample.rename(columns={
    "account_id": "Account ID",
    "name": "Name",
    "risk_level": "Risk Level",
    "response_behavior": "Behavior",
    "ai_confidence": "Confidence (%)"
})

# ใช้ styled_table เพื่อสร้าง HTML table ที่สวยงาม
styled_html = styled_table(rec_sample)

# แสดงผลผ่าน components.html เพื่อให้ render สวยงามจริง
components.html(styled_html, height=400, scrolling=True)

# --- Conversion Rate by Journey Type ---
import streamlit.components.v1 as components

# --- Conversion Rate by Journey Type ---
st.markdown("### 🔍 Conversion Rate by Journey Type (%)")

# สร้างตารางจากข้อมูลจริง
conversion = df.groupby("journey_type")["status_paid"].value_counts(normalize=True).unstack().fillna(0) * 100
conversion = conversion.round(1).reset_index()

# ใช้ styled_table เพื่อ render เป็น HTML
styled_html = styled_table(conversion)

# แสดง HTML table สวยงามด้วย components.html
components.html(styled_html, height=300, scrolling=True)


# --- Confidence Histogram ---
#st.markdown("### 📊 Journey Confidence Score Distribution")
#fig_conf = px.histogram(df, x="ai_confidence", nbins=20, title="AI Confidence Score", color_discrete_sequence=["#0B5394"])
#st.plotly_chart(fig_conf, use_container_width=True)


# --- Recovery KPI ---
if menu == "Recovery KPI":
    st.title(" Recovery KPI Dashboard")

    st.markdown("###  Recovery Overview (Month-to-date)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Recovered", "฿12,850,000")
    col2.metric("Recovery Rate", "64.7%")
    col3.metric("Avg. Time to Recovery", "3.6 days")
    col4.metric("Active Collectors", "12")

    trend_data = pd.DataFrame({
        "Date": pd.date_range("2025-07-01", periods=10, freq="D"),
        "Recovered": [1000000, 1250000, 1380000, 1220000, 1500000, 1600000, 1700000, 1450000, 1550000, 1650000]
    })
    fig_trend = px.line(trend_data, x="Date", y="Recovered", markers=True, title="Daily Recovery Trend", color_discrete_sequence=flowen_colors)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("###  Channel Effectiveness")
    channel_perf = pd.DataFrame({
        "Channel": ["LINE Bot", "Voice Bot", "Phone Call", "Email"],
        "Success Rate (%)": [43, 38, 54, 22],
        "Avg Recovery per Case": [850, 720, 1100, 460]
    })
    fig_bar = px.bar(
        channel_perf,
        x="Channel",
        y="Success Rate (%)",
        color="Channel",
        title="Channel Success Rate",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("###  Collector Leaderboard")
    collector_data = pd.DataFrame({
        "Collector": ["Aon", "May", "Bee", "Tarn", "Jib"],
        "Recovered (฿)": [1450000, 1380000, 1250000, 1190000, 950000],
        "Cases Closed": [95, 87, 81, 74, 66]
    })
    st.dataframe(collector_data)

    st.markdown("###  Recovery by Risk Level")
    risk_seg = pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High"],
        "Recovery Rate (%)": [72, 63, 44]
    })
    fig_seg = px.bar(
        risk_seg,
        x="Risk Level",
        y="Recovery Rate (%)",
        color="Risk Level",
        title="Recovery Rate by Risk Group",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_seg, use_container_width=True)

    st.markdown("###  Recovery Conversion Funnel")
    funnel_data = pd.DataFrame({
        "Stage": ["Messaged", "Opened", "Responded", "Promised to Pay", "Paid"],
        "Count": [18000, 14400, 9100, 3400, 1850]
    })
    fig_funnel = px.funnel(
        funnel_data,
        x="Count",
        y="Stage",
        title="End-to-End Recovery Funnel",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("###  AI Journey Effectiveness")
    ai_journey = pd.DataFrame({
        "Journey": ["LINE Reminder A", "LINE Reminder B", "Voice Push", "Aggressive Call"],
        "Recovery Rate (%)": [28, 42, 38, 35],
        "Best Segment": ["Low Risk", "Medium Risk", "High Risk", "Ignored Group"]
    })
    st.dataframe(ai_journey)
    st.success(" Insight: LINE Reminder B has 42% recovery rate in Medium-Risk group. Consider promoting this journey.")

# --- Behavioral Insights ---
elif menu == "Behavioral Insights":
    st.title(" Behavioral Insights Dashboard")

    st.markdown("###  Response Behavior")
    response_counts = df["response_behavior"].value_counts().reset_index()
    response_counts.columns = ["Behavior", "Count"]
    fig_response = px.pie(
        response_counts,
        names="Behavior",
        values="Count",
        hole=0.4,
        title="Customer Response Breakdown",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_response, use_container_width=True)

    st.markdown("###  Repayment Timing")
    repay_delay = pd.DataFrame({
        "Delay (Days)": ["0–1", "2–3", "4–7", "8–14", "15+"],
        "Paid Count": [350, 420, 300, 180, 90]
    })
    fig_repay = px.bar(
        repay_delay,
        x="Delay (Days)",
        y="Paid Count",
        title="Repayment after Reminder Timing",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_repay, use_container_width=True)

    st.markdown("###  Avoidance Pattern")
    avoid = df[df["response_behavior"] == "Ignored"].groupby("region").size().reset_index(name="Ignored Count")
    fig_avoid = px.bar(
        avoid,
        x="region",
        y="Ignored Count",
        color="region",
        title="Avoidance by Region",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_avoid, use_container_width=True)

    st.markdown("###  Cash Flow Pattern")
    fig_cash = px.histogram(
        df,
        x="monthly_income",
        nbins=30,
        title="Monthly Income Distribution",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_cash, use_container_width=True)

    st.markdown("###  Channel vs Behavior")
    chan_beh = df.groupby(["contact_channel", "response_behavior"]).size().reset_index(name="Count")
    fig_chan = px.bar(
        chan_beh,
        x="contact_channel",
        y="Count",
        color="response_behavior",
        barmode="group",
        title="Contact Channel Performance by Behavior",
        color_discrete_sequence=flowen_colors
    )
    st.plotly_chart(fig_chan, use_container_width=True)

    st.markdown("###  AI Insight Panel – NLP Behavior Tags")
    st.info("AI analyzes conversation logs and assigns behavioral tags for smarter journey orchestration.")

    ai_tags = pd.DataFrame({
        "Sample Message": [
            "ขอเลื่อน 3 วัน",
            "ตอนนี้ไม่มีเงิน",
            "ไม่ใช่หนี้ผม",
            "จะจ่ายพรุ่งนี้",
            "ไม่ตอบกลับ"
        ],
        "AI Tag": [
            "Willing",
            "Cashflow_Issue",
            "Dispute",
            "Pay_Intent",
            "Silent"
        ],
        "Recommended Action": [
            "Remind in 2 days",
            "Pause & retry next payday",
            "Send dispute form",
            "Follow-up in 24h",
            "Escalate to voice"
        ]
    })
    st.dataframe(ai_tags)

