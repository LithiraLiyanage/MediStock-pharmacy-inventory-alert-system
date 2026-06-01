import streamlit as st
from services.inventory_service import get_all_medicines, update_stock, get_stock_movements
from utils.validators import validate_stock_update
from utils.helpers import readable_table
from utils.styles import section_title


def show():
    st.markdown(section_title('🔄 Stock Update'), unsafe_allow_html=True)
    df = get_all_medicines()
    if df.empty:
        st.info('No medicines available.')
        return
    labels = {f"{r['medicine_name']} | Batch: {r['batch_number']} | Qty: {r['quantity']} | ID: {r['id']}": r for _, r in df.iterrows()}
    selected = st.selectbox('Select Medicine', [''] + list(labels.keys()))
    movement_type = st.selectbox('Movement Type', ['Stock In', 'Stock Out', 'Set Exact Stock'])
    amount = st.number_input('Quantity', min_value=0, step=1)
    note = st.text_area('Movement Note', max_chars=200)
    if st.button('Update Stock'):
        if not selected:
            st.error('Medicine must be selected.')
            return
        med = labels[selected]
        errors = validate_stock_update(med['id'], movement_type, amount, med['quantity'], note)
        if errors:
            for e in errors: st.error(e)
            return
        try:
            st.success(f"Stock updated successfully. New quantity: {update_stock(med['id'], movement_type, amount, note)}")
        except ValueError as e:
            st.error(str(e))
    st.markdown('### 🧾 Stock Movement History')
    moves = get_stock_movements()
    if moves.empty: st.info('No stock movements yet.')
    else: st.dataframe(readable_table(moves), use_container_width=True)
