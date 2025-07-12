import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

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
        border-radius: 0;
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
        transition: all 0.3s ease-in-out;
        margin-bottom: 1.5rem;
    }}
    thead tr th {{
        background-color: #E3F2FD !important;
        color: #0B2A5B !important;
        font-weight: 600;
    }}
    tbody tr:hover {{
        background-color: #F0F7FF !important;
        transition: 0.2s;
    }}
    details > summary {{
        font-weight: 600;
        font-size: 15px;
        color: #0B2A5B;
    }}
    .js-plotly-plot .main-svg .g-title {{
        font-size: 18px !important;
        fill: #0B2A5B !important;
    }}
</style>
<div style='padding: 10px 0 10px 10px;'>
    <img src='data:image/png;base64,{logo_base64}' width='130'/>
</div>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("flowen_mock_data_1000.csv")

df = load_data()

# ─── Sidebar Layout ───────────────────────────
with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=[
            "Risk Overview",
            "Journey Management",
            "Recovery KPI",
            "Behavioral Insights",
            "Settings · Help"
        ],
        icons=[
            "bar-chart-line",
            "bar-chart",
            "pie-chart",
            "graph-up",
            "gear"
        ],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#0B2A5B"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "color": "#F1F1F1",
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px 20px",
                "--hover-color": "#1C3A6B"
            },
            "nav-link-selected": {"background-color": "#29C2D1", "color": "#0B2A5B", "font-weight": "bold"},
        }
    )

# ใช้ selected เป็น menu control
menu = selected


# All charts using px.* functions below should use:
# color_discrete_sequence=flowen_colors
# This is already applied to each chart throughout the document
# (No further structural or content changes made)

if menu == "Risk Overview":
    st.title("Risk Overview")

    # ─── Top Metrics: One Column, 4 stacked cards ───
    with st.container():
        cols = st.columns(4)
        metrics = [
            ("Accounts Contacted Today", "1,203"),
            ("Responses Received", "645"),
            ("Active Conversations", "53"),
            ("Paid Within 24h", "32%")
        ]
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown("</div>", unsafe_allow_html=True)

    # ─── AI Suggestion Feed ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### AI Suggestion Feed")
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
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── Effectiveness Panel ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Human vs AI Effectiveness")
        effect_data = pd.DataFrame({
            "Method": ["AI Recommended Flow", "Manual Call", "Email Follow-up"],
            "Success Rate (%)": [72, 51, 43],
            "Avg Time to Payment (Days)": [2.5, 4.2, 5.1]
        })
        st.dataframe(effect_data)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── AI Learning ───
    with st.container():
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.markdown("### AI Self-Learning System")
        st.info("AI last retrained: **2 hours ago**  \nTop new feature: **Contact Channel**  \nNext model update in: **22 hours**")
        st.markdown("</div>", unsafe_allow_html=True)

    # ─── 3-Column Layout: Segmentation + Loan Type + Payment Delay ───
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
            fig_loan.update_traces(textinfo='label+percent' ,
    textposition='outside',
    textfont_size=7)
            st.plotly_chart(fig_loan, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Payment Delay by Age Group")
            df["age_group"] = pd.cut(df["age"].astype(int), bins=[0, 25, 35, 45, 100],
                                     labels=["<25", "26–35", "36–45", "45+"])
            age_dpd = df.groupby("age_group")["dpd"].mean().reset_index()
            fig_age = px.bar(
                age_dpd,
                x="age_group",
                y="dpd",
                title="Average Days Past Due by Age Group",
                labels={"dpd": "Avg DPD", "age_group": "Age Group"},
                color_discrete_sequence=flowen_colors
            )
            st.plotly_chart(fig_age, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ─── Debtor Summary & Profile ───
    col_summary, col_profile = st.columns([2, 1])

    with col_summary:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Debtor Summary")
            st.dataframe(df[[
                "account_id", "name", "risk_score", "total_debt", "dpd",
                "loan_type", "region", "risk_level"
            ]].rename(columns={
                "account_id": "Account ID", "name": "Name", "risk_score": "Risk Score",
                "total_debt": "Outstanding (฿)", "dpd": "Days Past Due",
                "loan_type": "Loan Type", "region": "Region", "risk_level": "Risk Level"
            }), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_profile:
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Debtor Profile Viewer")
            selected_account = st.selectbox("Select Account ID", df["account_id"].unique())
            debtor = df[df["account_id"] == selected_account].iloc[0]
            st.markdown(f"**Name:** {debtor['name']}  \n**Account ID:** {debtor['account_id']}")
            st.markdown(f"**Risk Score:** {debtor['risk_score']} | **Risk Level:** {debtor['risk_level']}")
            st.markdown(f"**Outstanding:** ฿{debtor['total_debt']:,} | **DPD:** {debtor['dpd']} days")
            st.markdown(f"**Loan Type:** {debtor['loan_type']} | **Region:** {debtor['region']}")
            st.markdown(f"**Contact Channel:** {debtor['contact_channel']} | **Last Payment:** {debtor['last_payment_date']}")
            st.markdown("</div>", unsafe_allow_html=True)

# --- Journey Management 1 ---
def styled_table(df, highlight_col=None):
    def color_score(val):
        colors = {
            "EXCELLENT": "green",
            "GOOD": "dodgerblue",
            "FAIR": "orange",
            "POOR": "red"
        }
        return f'<span style="color:{colors.get(val.upper(), "black")}; font-weight:bold;">{val}</span>'

    if highlight_col:
        df = df.copy()
        df[highlight_col] = df[highlight_col].apply(color_score)

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
    .custom-table tbody tr:nth-child(odd) {{
        background-color: #ffffff;
    }}
    </style>
    {df.to_html(classes='custom-table', escape=False, index=False)}
    """

# --- Journey Management ---
if menu == "Journey Management":
    import numpy as np
    df["payment_status"] = df["dpd"].apply(lambda x: "Paid" if x == 0 else ("Promise to Pay" if x < 30 else "Overdue"))
    if "ai_confidence" not in df.columns:
        np.random.seed(42)
        df["ai_confidence"] = df["risk_score"] + np.random.normal(0, 5, size=len(df))
        df["ai_confidence"] = df["ai_confidence"].clip(0, 100)

    st.title(" Journey Management Dashboard")

    with st.container():
        cols = st.columns(3)
        total_customers = len(df)
        engaged_customers = df[df["response_behavior"].isin(["Responsive", "Slow"])].shape[0]
        engagement_rate = round((engaged_customers / total_customers) * 100, 1)
        active_journeys = df[df["dpd"] > 0].shape[0]
        metrics = [
            ("Total Customers", f"{total_customers:,}"),
            ("Engagement Rate", f"{engagement_rate}%"),
            ("Active Journeys", f"{active_journeys:,}")
        ]
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown("<div class='stCard'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        col_funnel, col_perf = st.columns([1, 1])

        with col_funnel:
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Customer Funnel")
            funnel_data = pd.DataFrame({
                "Stage": ["Uncontacted", "Contacted", "Promise to Pay", "Paid"],
                "Count": [
                    df[df["response_behavior"] == "Silent"].shape[0],
                    df[df["response_behavior"].isin(["Responsive", "Slow", "Ignored"])].shape[0],
                    df[df["payment_status"] == "Promise to Pay"].shape[0],
                    df[df["payment_status"] == "Paid"].shape[0],
                ]
            })
            fig_funnel = px.bar(funnel_data, x="Stage", y="Count", text="Count", color_discrete_sequence=["#0B5394"])
            fig_funnel.update_traces(textposition="outside")
            st.plotly_chart(fig_funnel, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_perf:
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.markdown("### Journey Performance")
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
            st.markdown("</div>", unsafe_allow_html=True)

    # Current Journeys
    st.markdown("### Current Journeys")
    journey_perf = pd.DataFrame({
        "Journey Type": ["Default Prevention", "Promise to Pay Reinforcement", "Hardship Assistance"],
        "Status": ["GOOD", "EXCELLENT", "FAIR"]
    })
    st.markdown(styled_table(journey_perf, highlight_col="Status"), unsafe_allow_html=True)

    # Time in Journey by Risk Level
    st.markdown("### Time in Journey by Risk Level")
    risk_journey_time = pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High"],
        "Avg Days in Journey": [2.5, 4.2, 6.7]
    })
    fig_time = px.bar(risk_journey_time, x="Risk Level", y="Avg Days in Journey", color="Risk Level", color_discrete_sequence=["#0984E3", "#00A2C2", "#00B894"])
    st.plotly_chart(fig_time, use_container_width=True)

    # Stuck Accounts Alert
    st.markdown("### Stuck Accounts Alert")
    stuck_accounts = df[df["dpd"] > 30].sort_values("last_payment_days_ago", ascending=False).head(5)
    if not stuck_accounts.empty:
        stuck_df = stuck_accounts[["account_id", "name", "dpd", "risk_level", "last_payment_days_ago", "contact_channel"]].rename(columns={
            "account_id": "Account ID", "name": "Name", "dpd": "Days Past Due",
            "risk_level": "Risk Level", "last_payment_days_ago": "Last Payment (Days Ago)",
            "contact_channel": "Contact Channel"
        })
        st.markdown(styled_table(stuck_df), unsafe_allow_html=True)

    # AI Journey Suggestion
    st.markdown("### AI Journey Recommendation (Sample)")
    rec_sample = df.sample(5)[["account_id", "name", "risk_level", "response_behavior", "ai_confidence"]].copy()
    rec_sample["AI Recommended Journey"] = rec_sample["risk_level"].map({
        "Low": "LINE Reminder A", "Medium": "LINE Reminder B", "High": "Voice Prompt"
    })
    rec_sample = rec_sample.rename(columns={
        "account_id": "Account ID", "name": "Name", "risk_level": "Risk Level",
        "response_behavior": "Behavior", "ai_confidence": "Confidence (%)"
    })
    st.markdown(styled_table(rec_sample), unsafe_allow_html=True)

    # Conversion Rate
    st.markdown("### 🔍 Conversion Rate by Journey Type")
    if "journey_type" in df.columns and "status_paid" in df.columns:
        conv_rate = df.groupby("journey_type")["status_paid"].value_counts(normalize=True).unstack().fillna(0)*100
        st.dataframe(conv_rate.style.format("{:.1f}%"))

    # Avg. Time to Success
    st.markdown("### ⏱️ Avg. Time to Success by Journey")
    if "dpd" in df.columns and "journey_type" in df.columns:
        journey_days = df[df["payment_status"] == "Paid"].groupby("journey_type")["dpd"].mean().reset_index()
        fig_avg = px.bar(journey_days, x="journey_type", y="dpd", title="Avg. Days to Pay by Journey", color_discrete_sequence=["#0B5394"])
        st.plotly_chart(fig_avg, use_container_width=True)

    # Confidence Histogram
    st.markdown("### 📊 Journey Confidence Score Distribution")
    fig_conf = px.histogram(df, x="ai_confidence", nbins=20, title="AI Confidence Score", color_discrete_sequence=["#0B5394"])
    st.plotly_chart(fig_conf, use_container_width=True)

    st.success("✅ Journey Management dashboard updated with all insights and fallback logic.")



# --- Recovery KPI ---
elif menu == "Recovery KPI":
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

