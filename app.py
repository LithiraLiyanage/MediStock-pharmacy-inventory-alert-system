import streamlit as st
from database.db import init_db
from utils.styles import inject_css
from pages import landing, dashboard, add_medicine, inventory, stock_update, expiry_alerts, low_stock_alerts, analytics, export_reports, about

st.set_page_config(page_title='MediStock | Pharmacy Inventory Alert System', page_icon='💊', layout='wide', initial_sidebar_state='expanded')
inject_css(st)
init_db()

st.sidebar.markdown('## 💊 MediStock')
st.sidebar.markdown('### Pharmacy Inventory')
st.sidebar.markdown('---')

pages = {
    '🏠 Landing Page': landing.show,
    '📊 Dashboard': dashboard.show,
    '💊 Add Medicine': add_medicine.show,
    '📦 Inventory': inventory.show,
    '🔄 Stock Update': stock_update.show,
    '⏳ Expiry Alerts': expiry_alerts.show,
    '🚨 Low Stock Alerts': low_stock_alerts.show,
    '📈 Analytics': analytics.show,
    '🧾 Export Reports': export_reports.show,
    'ℹ️ About Project': about.show,
}
# allow navigation via ?nav=<label> links so landing cards can navigate programmatically
selected = st.sidebar.radio('Navigate', list(pages.keys()))
st.sidebar.markdown('---')
st.sidebar.info('Educational inventory management project only. No medical diagnosis or treatment advice.')
pages[selected]()
