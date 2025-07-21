# Flowen: AI Debt Collection Dashboard (PoC)

This project is a fully functional Proof of Concept (PoC) of an AI-powered debt collection dashboard for banks and NBFCs. It integrates real-time risk scoring, behavioral analytics, journey orchestration, and interactive dashboards built with Streamlit.

## 📊 Key Features

- Risk Scoring Dashboard: Risk segmentation, recovery analysis, and AI insights
- Journey Management: Current journey status, AI recommendation, confidence score, funnel tracking
- Recovery KPI: Daily recovery trend, channel effectiveness, collector leaderboard
- Behavioral Insights: Response behavior, repayment patterns, income, channel vs behavior
- Debtor Profile View: Click to view detailed profile and contact info
- Language Toggle: 🇬🇧 / 🇹🇭
- Theming: Custom color scheme based on Flowen brand
- Data Export: PDF/Excel (optional enhancement)
- Notifications: (Placeholder - real-time alerts logic ready)
- Voice & LINE Bot scripts: Draft sample included

## 📁 File Structure

flowen-poc/
│
├── app.py # Main launcher
├── pages/
│ ├── 1_Risk_Overview.py
│ ├── 2_Journey_Management.py
│ ├── 3_Recovery_KPI.py
│ └── 4_Behavioral_Insights.py
│
├── utils/
│ └── charts.py # Common Plotly chart configs
├── flowen_logo.png
├── flowen_mock_data_5000_enhanced.csv
├── README.md
└── TOR.txt


## 🧠 Data Overview

Mock data file: `flowen_mock_data_5000_enhanced.csv`

- `account_id`, `name`, `age`, `region`, `loan_type`
- `dpd`, `total_debt`, `monthly_income`
- `contact_channel`, `response_behavior`, `last_payment_date`, `last_contact_date`
- `risk_score`, `risk_level`, `ai_risk_score`, `ai_confidence`
- `journey_type`, `status_paid`, `recovered`
- Extra behavior and clustering-ready fields included

## 🚀 Quick Start (Local)

```bash
pip install -r requirements.txt
streamlit run app.py


