import streamlit as st
from services.inventory_service import get_low_stock_medicines
from utils.helpers import readable_table
from utils.styles import section_title, alert_card


def show():
    st.markdown(section_title('🚨 Low Stock Alerts'), unsafe_allow_html=True)
    low = get_low_stock_medicines()
    if low.empty:
        st.markdown(alert_card('No low-stock medicines found.', 'success'), unsafe_allow_html=True)
        return
    critical = low[low['urgency'] == 'Critical']
    high = low[low['urgency'] == 'High']
    medium = low[low['urgency'] == 'Medium']
    c1, c2, c3 = st.columns(3)
    c1.error(f'Critical: {len(critical)}')
    c2.warning(f'High: {len(high)}')
    c3.info(f'Medium: {len(medium)}')
    st.dataframe(readable_table(low.sort_values(['urgency', 'quantity'])), use_container_width=True)
