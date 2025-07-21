import streamlit as st
import pandas as pd
import plotly.express as px
from utils.notification import render_notification_bar
from utils.language import get_text

# --- Load Data ---
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# --- Language Toggle ---
if "lang" not in st.session_state:
    st.session_state["lang"] = "EN"
lang = st.session_state["lang"]

# --- Page Config ---
st.set_page_config(page_title="Flowen | Risk Overview", layout="wide")

# --- Sidebar Logo & Language ---
st.sidebar.image("assets/flowen_logo.png", use_column_width=True)
lang_option = st.sidebar.selectbox("Language", ["EN", "TH"], index=0 if lang == "EN" else 1)
st.session_state["lang"] = lang_option

# --- Notification ---
render_notification_bar(lang)

# --- Title ---
st.title(get_text("Risk Overview", lang))

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
col1.metric(label=get_text("Total Debtors", lang), value=f"{len(df):,}")
col2.metric(label=get_text("Average DPD", lang), value=f"{df['dpd'].mean():.1f}")
col3.metric(label=get_text("High Risk %", lang), value=f"{(df['ai_risk_score'] > 0.7).mean() * 100:.1f}%")

# --- Charts ---
st.subheader(get_text("Risk Segmentation", lang))
col4, col5, col6 = st.columns(3)

with col4:
    risk_group = df['clustering_group'].value_counts().reset_index()
    fig1 = px.pie(risk_group, names='index', values='clustering_group',
                 title=get_text("Clustering Segments", lang), hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    by_loan = df.groupby("loan_type").size().reset_index(name='count')
    fig2 = px.bar(by_loan, x='loan_type', y='count', color='loan_type',
                  title=get_text("Loan Type Breakdown", lang))
    st.plotly_chart(fig2, use_container_width=True)

with col6:
    by_age = df['age_group'].value_counts().reset_index()
    fig3 = px.bar(by_age, x='index', y='age_group',
                  title=get_text("Age Group Distribution", lang))
    st.plotly_chart(fig3, use_container_width=True)

# --- Debtor Table ---
st.subheader(get_text("Debtor Table", lang))
st.dataframe(df[["debtor_id", "name", "dpd", "ai_risk_score", "loan_type", "clustering_group"]].head(20))

# TODO: Add click to open Debtor Profile View when integrated
