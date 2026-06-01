import streamlit as st
from services.inventory_service import get_all_medicines, get_low_stock_medicines
from services.analytics_service import category_chart, value_chart, expiry_pie, low_stock_urgency_chart, monthly_expiry_chart
from utils.helpers import readable_table
from utils.styles import section_title


def show():
    st.markdown(section_title('📊 Analytics'), unsafe_allow_html=True)
    df = get_all_medicines()
    low = get_low_stock_medicines()
    if df.empty:
        st.info('No data available for analytics.')
        return
    c1, c2 = st.columns(2)
    with c1:
        fig = category_chart(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = value_chart(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        fig = expiry_pie(df)
        if fig: st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = low_stock_urgency_chart(low)
        if fig: st.plotly_chart(fig, use_container_width=True)
        else: st.success('No low-stock urgency data.')
    fig = monthly_expiry_chart(df)
    if fig: st.plotly_chart(fig, use_container_width=True)
    st.markdown('### 💰 Top 10 Most Valuable Medicines')
    st.dataframe(readable_table(df.sort_values('stock_value', ascending=False).head(10)), use_container_width=True)
    st.markdown('### 📉 Top 10 Lowest Stock Medicines')
    st.dataframe(readable_table(df.sort_values('quantity').head(10)), use_container_width=True)
