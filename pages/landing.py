import streamlit as st
import urllib.parse
from services.analytics_service import dashboard_metrics
from utils.helpers import money
from utils.styles import metric_card, footer


def show():
    m = dashboard_metrics()
    # create simple nav links that point to Streamlit page routes
    dash_link = '/dashboard'
    add_link = '/add_medicine'
    alerts_link = '/low_stock_alerts'

    hero = f"""
    <div class="hero">
      <div class="hero-grid">
        <div>
          <div style="font-weight:900;color:#FFE4E6;">💊 PHARMACY INVENTORY DASHBOARD</div>
          <h1>MediStock</h1>
          <h3 style="color:white;">Smart Pharmacy Inventory & Expiry Alert System</h3>
          <p>Track medicine stock, batch expiry dates, low-stock alerts, and pharmacy analytics from one clean dashboard.</p>
          <div style="margin-top:1.5rem;display:flex;gap:.8rem;flex-wrap:wrap;">
            <a href="{dash_link}" style="text-decoration:none"><span class="badge" style="background:white;color:#DC2626;">📊 Open Dashboard</span></a>
            <a href="{add_link}" style="text-decoration:none"><span class="badge" style="background:#FFE4E6;color:#991B1B;">💊 Add Medicine</span></a>
            <a href="{alerts_link}" style="text-decoration:none"><span class="badge" style="background:#FECACA;color:#7F1D1D;">🚨 View Alerts</span></a>
          </div>
        </div>
        <div class="mock-card">
          <h3 style="color:white;">🏥 Live Inventory Pulse</h3>
          <div class="mock-row"><span>Total Medicines</span><b>{m['total_medicines']}</b></div>
          <div class="mock-row"><span>Low Stock</span><b>{m['low_stock_count']}</b></div>
          <div class="mock-row"><span>Near Expiry</span><b>{m['near_expiry_count']}</b></div>
          <div class="mock-row"><span>Expired</span><b>{m['expired_count']}</b></div>
        </div>
      </div>
    </div>
    """
    st.markdown(hero, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card('Medicine Inventory', m['total_medicines'], '💊'), unsafe_allow_html=True)
    c2.markdown(metric_card('Stock Quantity', m['total_quantity'], '📦'), unsafe_allow_html=True)
    c3.markdown(metric_card('Inventory Value', money(m['inventory_value']), '💰'), unsafe_allow_html=True)
    c4.markdown(metric_card('Active Alerts', m['low_stock_count'] + m['expired_count'] + m['near_expiry_count'], '🚨'), unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ What MediStock Can Do</div>', unsafe_allow_html=True)
    # features with direct route paths so clicking navigates to that page
    features = [
      ('🏷️ Batch Tracking', 'Track each medicine by batch number and expiry date.', '/inventory'),
      ('🚨 Low Stock Alerts', 'Find medicines that need reorder before stock runs out.', '/low_stock_alerts'),
      ('⏳ Expiry Alerts', 'Monitor expired and near-expiry medicines safely.', '/expiry_alerts'),
      ('🔍 Inventory Search', 'Search, filter, and sort medicine records quickly.', '/inventory'),
      ('📊 Stock Analytics', 'Understand inventory value, categories, and risk areas.', '/analytics'),
      ('🧾 CSV Reports', 'Download inventory, low-stock, and expiry reports.', '/export_reports'),
    ]
    cols = st.columns(3)
    for i, (title, text, route) in enumerate(features):
      card_html = f'<a href="{route}" style="text-decoration:none;color:inherit;"><div class="feature-card"><h3>{title}</h3><p>{text}</p></div></a>'
      cols[i % 3].markdown(card_html, unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)
