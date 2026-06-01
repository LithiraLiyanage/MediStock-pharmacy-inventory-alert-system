import streamlit as st
from datetime import date
from services.inventory_service import add_medicine, duplicate_exists
from utils.validators import validate_medicine, CATEGORIES
from utils.styles import section_title


def show():
    st.markdown(section_title('💊 Add New Medicine'), unsafe_allow_html=True)
    st.info('Inventory management only. No dosage, diagnosis, or treatment advice.')
    with st.form('add_medicine_form'):
        c1, c2 = st.columns(2)
        medicine_name = c1.text_input('Medicine Name *')
        generic_name = c2.text_input('Generic Name')
        c3, c4 = st.columns(2)
        category = c3.selectbox('Category *', CATEGORIES)
        batch_number = c4.text_input('Batch Number *')
        c5, c6 = st.columns(2)
        supplier_name = c5.text_input('Supplier Name')
        storage_location = c6.text_input('Storage Location')
        c7, c8, c9 = st.columns(3)
        quantity = c7.number_input('Quantity *', min_value=0, step=1)
        unit_price = c8.number_input('Unit Price *', min_value=0.0, step=0.5)
        reorder_level = c9.number_input('Reorder Level *', min_value=0, step=1)
        expiry_date = st.date_input('Expiry Date *', value=date.today())
        notes = st.text_area('Notes', max_chars=300)
        submitted = st.form_submit_button('💊 Add Medicine')
    if submitted:
        data = dict(medicine_name=medicine_name, generic_name=generic_name, category=category, batch_number=batch_number, supplier_name=supplier_name, quantity=quantity, unit_price=unit_price, expiry_date=expiry_date, reorder_level=reorder_level, storage_location=storage_location, notes=notes)
        dup = duplicate_exists(medicine_name.strip(), batch_number.strip())
        errors, warnings = validate_medicine(data, dup)
        for w in warnings: st.warning(w)
        if errors:
            for e in errors: st.error(e)
            return
        try:
            add_medicine(data)
            st.success('Medicine added successfully.')
        except ValueError as e:
            st.error(str(e))
