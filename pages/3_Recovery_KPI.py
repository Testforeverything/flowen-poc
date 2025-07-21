import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")
lang = st.session_state.get("lang", "🇬🇧 EN")
st.session_state["lang"] = lang

# Notification bar
if lang == "🇬🇧 EN":
    st.info("📈 Updated recovery performance available.")
else:
    st.info("📈 อัปเดตประสิทธิภาพการติดตามแล้ว")

# Title
st.title("📈 Recovery KPI" if lang == "🇬🇧 EN" else "📈 ตัวชี้วัดการกู้คืนหนี้")

# KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Recovered" if lang == "🇬🇧 EN" else "ยอดกู้คืนรวม", f"฿{df['recovered_amount'].sum():,.0f}")
col2.metric("Avg Recovery per Account", f"฿{df['recovered_amount'].mean():,.2f}")
col3.metric("% Fully Paid", f"{(df['recovered_amount'] >= df['outstanding_balance']).mean() * 100:.1f}%")

# Recovery by channel (Bar chart)
recovery_by_channel = df.groupby('channel_used')['recovered_amount'].sum().reset_index()
recovery_by_channel.columns = ['Channel', 'Recovered']
fig1 = px.bar(recovery_by_channel, x='Channel', y='Recovered', text='Recovered',
              title="Recovery by Channel" if lang == "🇬🇧 EN" else "การกู้คืนแยกตามช่องทาง")
fig1.update_traces(texttemplate='฿%{text:,.0f}', textposition='outside')
fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig1, use_container_width=True)

# Daily recovery (Line chart)
if 'followup_date' in df.columns:
    df['followup_date'] = pd.to_datetime(df['followup_date'], errors='coerce')
    recovery_by_day = df.groupby(df['followup_date'].dt.date)['recovered_amount'].sum().reset_index()
    recovery_by_day.columns = ['Date', 'Recovered']
    fig2 = px.line(recovery_by_day, x='Date', y='Recovered',
                   title="Daily Recovery Trend" if lang == "🇬🇧 EN" else "แนวโน้มการกู้คืนรายวัน")
    st.plotly_chart(fig2, use_container_width=True)

# Export section
st.download_button("📥 Export KPI Data", data=df.to_csv(index=False),
                   file_name="recovery_kpi_export.csv")
