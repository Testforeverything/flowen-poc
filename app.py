import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Session State ───
if "lang" not in st.session_state:
    st.session_state["lang"] = "🇬🇧 English"
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

lang = st.session_state["lang"]

# ─── Sidebar Navigation ───
st.sidebar.image("assets/flowen_logo.png", width=200)
st.sidebar.title("Flowen Dashboard")

menu = st.sidebar.radio(
    "🔍 Navigate to",
    [
        "Home",
        "Risk Overview",
        "Journey Management",
        "Recovery KPI",
        "Behavioral Insights"
    ]
)
st.session_state["page"] = menu

# ─── Language Toggle ───
lang_option = st.sidebar.selectbox("🌐 Language / ภาษา", ["🇬🇧 English", "🇹🇭 ไทย"])
st.session_state["lang"] = lang_option
lang = lang_option

# ─── Real-Time Notification ───
if lang == "🇬🇧 English":
    st.markdown("📢 Welcome back! Use the menu to explore Flowen modules.")
else:
    st.markdown("📢 ยินดีต้อนรับ! ใช้เมนูด้านซ้ายเพื่อเข้าสู่แต่ละโมดูล")

# ─── Load Data ───
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ─── Page Rendering ───

if menu == "Home":
    st.title("👋 Welcome to Flowen" if lang == "🇬🇧 English" else "👋 ยินดีต้อนรับสู่ Flowen")
    st.markdown(
        "Your AI-driven debt collection assistant."
        if lang == "🇬🇧 English"
        else "ผู้ช่วย AI ด้านการติดตามหนี้ของคุณ"
    )
    st.image("assets/flowen_logo.png", width=300)
    st.success("Select a module on the left to begin." if lang == "🇬🇧 English" else "เลือกโมดูลจากด้านซ้ายเพื่อเริ่มต้นใช้งาน")

elif menu == "Risk Overview":
    st.title("📊 Risk Overview" if lang == "🇬🇧 English" else "📊 ภาพรวมความเสี่ยง")

    risk_count = df["risk_score"].value_counts().sort_index()
    fig = px.bar(
        x=risk_count.index,
        y=risk_count.values,
        labels={"x": "Risk Score", "y": "Number of Accounts"},
        title="Risk Score Distribution" if lang == "🇬🇧 English" else "การกระจายของคะแนนความเสี่ยง",
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Journey Management":
    st.title("🧭 Journey Management" if lang == "🇬🇧 English" else "🧭 จัดการเส้นทางติดตาม")

    st.markdown(
        "- Segment high-risk accounts\n"
        "- Recommend personalized follow-up journey\n"
        "- Auto tag and escalate"
    )

    st.dataframe(df[["account_id", "risk_score", "ai_risk_score", "response_behavior"]].head(10))

elif menu == "Recovery KPI":
    st.title("📈 Recovery KPI" if lang == "🇬🇧 English" else "📈 ตัวชี้วัดการกู้คืนหนี้")

    recovery_mock = pd.DataFrame({
        "Channel": ["Voice", "LINE", "SMS", "Email"],
        "Recovered": [85000, 105000, 62000, 45000]
    })

    fig = px.bar(
        recovery_mock,
        x="Channel",
        y="Recovered",
        title="Recovery by Channel" if lang == "🇬🇧 English" else "ยอดการกู้คืนตามช่องทาง",
        text="Recovered"
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Behavioral Insights":
    st.title("🧠 Behavioral Insights" if lang == "🇬🇧 English" else "🧠 การวิเคราะห์พฤติกรรม")

    st.markdown("### Cluster Groups" if lang == "🇬🇧 English" else "### กลุ่มพฤติกรรม")
    fig = px.histogram(df, x="clustering_group", color="clustering_group")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[["account_id", "loan_type", "dpd", "clustering_group"]].sample(10))
