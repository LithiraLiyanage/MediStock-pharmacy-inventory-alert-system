import streamlit as st
from services.inventory_service import get_all_medicines, get_low_stock_medicines, get_expired_medicines, get_near_expiry_medicines
from services.export_service import csv_bytes, timestamped_filename
from utils.helpers import readable_table
from utils.styles import section_title


def report_button(label, df, prefix):
    if df.empty:
        st.info(f'No data for {label}.')
        return
    st.dataframe(readable_table(df.head(20)), use_container_width=True)
    st.download_button(label=f'⬇️ Download {label}', data=csv_bytes(df), file_name=timestamped_filename(prefix), mime='text/csv')


def show():
    st.markdown(section_title('🧾 Export Reports'), unsafe_allow_html=True)
    near_days = st.slider('Near-expiry threshold for export', 7, 180, 30)
    tabs = st.tabs(['Full Inventory', 'Low Stock', 'Expired', 'Near Expiry', 'Stock Summary'])
    with tabs[0]: report_button('Full Inventory CSV', get_all_medicines(), 'full_inventory')
    with tabs[1]: report_button('Low Stock CSV', get_low_stock_medicines(), 'low_stock')
    with tabs[2]: report_button('Expired Medicines CSV', get_expired_medicines(), 'expired_medicines')
    with tabs[3]: report_button('Near Expiry CSV', get_near_expiry_medicines(near_days), 'near_expiry')
    with tabs[4]:
        df = get_all_medicines()
        if df.empty:
            st.info('No data.')
        else:
            summary = df.groupby('category', as_index=False).agg(medicine_count=('id', 'count'), total_quantity=('quantity', 'sum'), total_value=('stock_value', 'sum'))
            report_button('Stock Summary CSV', summary, 'stock_summary')
