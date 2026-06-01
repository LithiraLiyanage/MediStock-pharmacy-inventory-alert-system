import streamlit as st
from services.inventory_service import get_expired_medicines, get_near_expiry_medicines
from utils.helpers import readable_table
from utils.styles import section_title, alert_card


def show():
    st.markdown(section_title('⏳ Expiry Alerts'), unsafe_allow_html=True)
    threshold = st.slider('Near-expiry threshold days', 7, 180, 30)
    expired = get_expired_medicines()
    near = get_near_expiry_medicines(threshold)
    st.markdown('### 🚨 Expired Medicines')
    if expired.empty:
        st.markdown(alert_card('No expired medicines found.', 'success'), unsafe_allow_html=True)
    else:
        st.markdown(alert_card(f'{len(expired)} expired medicine batch(es) found.', 'danger'), unsafe_allow_html=True)
        st.dataframe(readable_table(expired.sort_values('days_remaining')), use_container_width=True)
    st.markdown('### ⚠️ Near-Expiry Medicines')
    if near.empty:
        st.markdown(alert_card('No near-expiry medicines found.', 'success'), unsafe_allow_html=True)
    else:
        st.markdown(alert_card(f'{len(near)} medicine batch(es) expire within {threshold} days.', 'warning'), unsafe_allow_html=True)
        st.dataframe(readable_table(near.sort_values('days_remaining')), use_container_width=True)
