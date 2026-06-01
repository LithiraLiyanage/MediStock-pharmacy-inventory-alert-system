import streamlit as st
from services.inventory_service import filter_medicines, get_all_medicines, delete_medicine
from utils.helpers import readable_table
from utils.styles import section_title


def show():
    st.markdown(section_title('📦 Medicine Inventory'), unsafe_allow_html=True)
    all_df = get_all_medicines()
    if all_df.empty:
        st.info('No medicines found.')
        return
    c1, c2, c3, c4 = st.columns(4)
    search = c1.text_input('Search')
    category = c2.selectbox('Category', ['All'] + sorted(all_df['category'].dropna().unique().tolist()))
    supplier = c3.selectbox('Supplier', ['All'] + sorted(all_df['supplier_name'].fillna('').unique().tolist()))
    status = c4.selectbox('Status', ['All', 'In Stock', 'Low Stock', 'Out of Stock', 'Near Expiry', 'Expired'])
    df = filter_medicines(search, category, supplier, status)
    if df.empty:
        st.warning('No records match your search/filter.')
        return
    sort = st.selectbox('Sort By', ['medicine_name', 'expiry_date', 'quantity', 'stock_value'])
    df = df.sort_values(sort)
    st.dataframe(readable_table(df), use_container_width=True)
    st.markdown('### 🗑️ Delete Medicine')
    ids = {f"{r['medicine_name']} | Batch: {r['batch_number']} | ID: {r['id']}": r['id'] for _, r in df.iterrows()}
    selected = st.selectbox('Select medicine to delete', [''] + list(ids.keys()))
    confirm = st.checkbox('I confirm this deletion')
    if st.button('Delete Selected Medicine'):
        if not selected: st.error('Select a medicine first.')
        elif not confirm: st.error('Please confirm deletion.')
        else:
            delete_medicine(ids[selected])
            st.success('Medicine deleted successfully.')
            st.rerun()
