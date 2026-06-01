import streamlit as st
from services.analytics_service import dashboard_metrics, category_chart, value_chart, monthly_expiry_chart
from services.inventory_service import get_all_medicines, get_low_stock_medicines
from utils.helpers import money, readable_table
from utils.styles import metric_card, section_title


def show():
    st.markdown(section_title('📊 Pharmacy Dashboard'), unsafe_allow_html=True)
    df = get_all_medicines()
    m = dashboard_metrics()
    cols = st.columns(4)
    cols[0].markdown(metric_card('Total Medicines', m['total_medicines'], '💊'), unsafe_allow_html=True)
    cols[1].markdown(metric_card('Total Quantity', m['total_quantity'], '📦'), unsafe_allow_html=True)
    cols[2].markdown(metric_card('Inventory Value', money(m['inventory_value']), '💰'), unsafe_allow_html=True)
    cols[3].markdown(metric_card('Categories', m['categories_count'], '🧰'), unsafe_allow_html=True)
    cols = st.columns(4)
    cols[0].markdown(metric_card('Low Stock', m['low_stock_count'], '⚠️'), unsafe_allow_html=True)
    cols[1].markdown(metric_card('Out of Stock', m['out_of_stock_count'], '🚫'), unsafe_allow_html=True)
    cols[2].markdown(metric_card('Expired', m['expired_count'], '🚨'), unsafe_allow_html=True)
    cols[3].markdown(metric_card('Near Expiry', m['near_expiry_count'], '⏳'), unsafe_allow_html=True)
    if df.empty:
        st.info('No medicine records found.')
        return
    st.markdown('### 🕘 Recent Medicines')
    st.dataframe(readable_table(df.sort_values('created_at', ascending=False).head(8)), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        fig = category_chart(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = value_chart(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    fig = monthly_expiry_chart(df)
    if fig: st.plotly_chart(fig, use_container_width=True)
    low = get_low_stock_medicines()
    st.markdown('### 🚨 Top Low-Stock Medicines')
    if low.empty:
        st.success('No low-stock medicines found.')
    else:
        st.dataframe(readable_table(low.sort_values('quantity').head(10)), use_container_width=True)
