import streamlit as st
import pandas as pd

# โหลดข้อมูล
df = pd.read_csv("flowen_mock_data_5000_enhanced.csv")

# ตรวจสอบว่ามี customer_id ที่ส่งมาหรือไม่
if "selected_customer_id" not in st.session_state:
    st.warning("⚠️ กรุณาเลือกลูกหนี้จากหน้า Dashboard ก่อน")
    st.stop()

customer_id = st.session_state["selected_customer_id"]
debtor = df[df["customer_id"] == customer_id].iloc[0]
lang = st.session_state.get("lang", "🇬🇧 EN")

st.set_page_config(page_title="Debtor Profile", layout="centered")

# Header
st.title("👤 Debtor Profile" if lang == "🇬🇧 EN" else "👤 โปรไฟล์ลูกหนี้")
st.markdown(f"**Customer ID:** `{customer_id}`")

# สรุป Risk Score
st.metric(label="AI Risk Score", value=f"{debtor['ai_risk_score']:.2f}")
st.metric(label="Confidence", value=f"{debtor['ai_confidence']:.1%}")
st.metric(label="Current DPD", value=int(debtor['dpd']))

# ช่องทางการติดต่อ
st.subheader("📞 Contact Info" if lang == "🇬🇧 EN" else "📞 ช่องทางติดต่อ")
contact_cols = st.columns(2)
contact_cols[0].markdown(f"- **Phone:** {debtor.get('phone_number', '-')}")
contact_cols[0].markdown(f"- **Email:** {debtor.get('email', '-')}")
contact_cols[1].markdown(f"- **LINE ID:** {debtor.get('line_id', '-')}")
contact_cols[1].markdown(f"- **Region:** {debtor.get('region', '-')}")

st.markdown(f"- **Address:** {debtor.get('address', '-')}")
st.markdown(f"- **Work Address:** {debtor.get('work_address', '-')}")
st.markdown(f"- **Emergency Contact:** {debtor.get('emergency_contact', '-')}")

# พฤติกรรม
st.subheader("🧠 Behavior History" if lang == "🇬🇧 EN" else "🧠 พฤติกรรมลูกหนี้")
st.info(debtor['response_behavior'])

# Journey Assignment
st.subheader("📍 Assign to Journey" if lang == "🇬🇧 EN" else "📍 เลือกกลยุทธ์ติดตาม")
if st.button("📤 Send to AI Journey"):
    st.success("✅ Sent to Journey! (mocked)")
