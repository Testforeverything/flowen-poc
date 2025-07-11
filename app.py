import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('flowen_mock_data_1000.csv')

# Language toggle
lang = st.sidebar.selectbox("Language / ภาษา", ["English", "ไทย"])

# Title
st.title("Flowen - Debt Management Dashboard" if lang == "English" else "Flowen - แดชบอร์ดบริหารการติดตามหนี้")

# KPI Summary
if lang == "English":
    st.subheader("📊 Portfolio Overview")
    st.metric("Total Accounts", len(df))
    st.metric("Average Risk Score", round(df['ai_risk_score'].mean(), 2))
else:
    st.subheader("📊 ภาพรวมพอร์ต")
    st.metric("จำนวนบัญชีทั้งหมด", len(df))
    st.metric("คะแนนความเสี่ยงเฉลี่ย", round(df['ai_risk_score'].mean(), 2))

# Risk Score Distribution
fig_risk = px.histogram(df, x='ai_risk_score', nbins=20, title='Risk Score Distribution')
st.plotly_chart(fig_risk)

# DPD vs Risk Score
fig_dpd = px.scatter(df, x='dpd', y='ai_risk_score', color='dpd_bucket', title='DPD vs AI Risk Score')
st.plotly_chart(fig_dpd)

# Filterable table
st.subheader("Debtor Table")
filtered_df = df[['account_id', 'loan_type', 'dpd', 'dpd_bucket', 'ai_risk_score', 'risk_level', 'income_level']]
st.dataframe(filtered_df)
