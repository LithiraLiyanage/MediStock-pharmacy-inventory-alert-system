import streamlit as st
from utils.styles import section_title, footer


def show():
    st.markdown(section_title('🏥 About MediStock'), unsafe_allow_html=True)
    st.markdown('<div class="red-card"><h3>💊 MediStock — Pharmacy Inventory Alert System</h3><p>MediStock is a Python Streamlit mini project for pharmacy inventory management. It tracks medicine batches, expiry dates, quantities, reorder levels, stock movements, analytics, and CSV reports.</p></div>', unsafe_allow_html=True)
    st.markdown('### 🧰 Tech Stack')
    st.markdown('- Python 3.10+\n- Streamlit\n- SQLite\n- pandas\n- Plotly\n- CSV export')
    st.markdown('### ⚠️ Safety Scope')
    st.warning('Inventory management only. No diagnosis, treatment advice, dosage recommendations, drug interaction advice, or emergency guidance.')
    st.markdown('### 📌 CV Bullet')
    st.info('Developed MediStock, a Python Streamlit pharmacy inventory dashboard that tracks medicine batches, expiry dates, stock quantities, low-stock alerts, expired medicines, inventory analytics, and CSV reports using SQLite and pandas.')
    st.markdown('### 🚀 Future Improvements')
    st.markdown('- User login\n- Barcode scanning\n- OCR expiry date detection\n- PDF reports\n- Email/SMS alerts\n- Supplier management\n- Multi-branch pharmacy support\n- Docker deployment')
    st.markdown(footer(), unsafe_allow_html=True)
