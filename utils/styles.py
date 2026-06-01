def inject_css(st):
    st.markdown("""
    <style>
    .stApp{background:linear-gradient(180deg,#fff 0%,#FEF2F2 100%)}
    section[data-testid="stSidebar"]{background:linear-gradient(180deg,#7F1D1D 0%,#991B1B 45%,#DC2626 100%)!important} section[data-testid="stSidebar"] *{color:white!important}
    .main .block-container{padding-top:1.5rem;max-width:1280px}.hero{padding:3rem;border-radius:32px;background:linear-gradient(135deg,#7F1D1D 0%,#DC2626 50%,#F43F5E 100%);color:white;box-shadow:0 30px 70px rgba(220,38,38,.28);margin-bottom:1.5rem}.hero h1{font-size:4rem;font-weight:900;margin-bottom:.5rem;color:white}.hero p{color:#FFE4E6;font-size:1.1rem}.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:2rem;align-items:center}.mock-card{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.25);border-radius:28px;padding:1.5rem;backdrop-filter:blur(10px)}.mock-row{display:flex;justify-content:space-between;align-items:center;padding:.75rem 0;border-bottom:1px solid rgba(255,255,255,.14)}
    .metric-card{background:white;border:1px solid #FECACA;border-radius:22px;padding:1.25rem;box-shadow:0 18px 45px rgba(220,38,38,.08);margin-bottom:.75rem}.metric-label{color:#6B7280;font-size:.88rem;font-weight:700}.metric-value{color:#111827;font-size:2rem;font-weight:900;margin-top:.2rem}.section-title{background:linear-gradient(90deg,#DC2626,#F43F5E);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;font-size:2rem;margin:1rem 0}.red-card,.feature-card{background:white;border:1px solid #FECACA;border-radius:22px;padding:1.2rem;box-shadow:0 16px 38px rgba(185,28,28,.08);margin-bottom:1rem}.feature-card{background:linear-gradient(180deg,#fff 0%,#FEF2F2 100%)}.badge{display:inline-block;border-radius:999px;padding:.35rem .75rem;font-size:.78rem;font-weight:900}
    /* UI polish: disable accidental text selection and add hover states */
    .feature-card, .feature-card *, .badge, .metric-card, .metric-card * { user-select: none; -webkit-user-select: none; -ms-user-select: none; }
    a > .feature-card{cursor:pointer;transition:transform .18s ease, box-shadow .18s ease;display:block}
    a > .feature-card:hover{transform:translateY(-6px);box-shadow:0 30px 70px rgba(220,38,38,.28)}
    a{color:inherit;text-decoration:none}
    .feature-card h3{margin:0 0 .5rem 0}
    .feature-card p{margin:0;color:#6b7280}

    .alert-danger{background:#FEE2E2;border:1px solid #FCA5A5;color:#7F1D1D;padding:1rem;border-radius:18px;font-weight:700;margin-bottom:.8rem}.alert-warning{background:#FEF3C7;border:1px solid #FCD34D;color:#92400E;padding:1rem;border-radius:18px;font-weight:700;margin-bottom:.8rem}.alert-success{background:#DCFCE7;border:1px solid #86EFAC;color:#166534;padding:1rem;border-radius:18px;font-weight:700;margin-bottom:.8rem}.footer{margin-top:2rem;padding:1rem;text-align:center;color:#6B7280;border-top:1px solid #FECACA} div.stButton>button,div.stDownloadButton>button{background:linear-gradient(90deg,#DC2626,#F43F5E)!important;color:white!important;border:0!important;border-radius:14px!important;font-weight:800!important;box-shadow:0 12px 25px rgba(220,38,38,.20)}@media(max-width:900px){.hero-grid{grid-template-columns:1fr}.hero h1{font-size:2.8rem}}
    </style>
    """,unsafe_allow_html=True)
def metric_card(title,value,icon='💊'): return f'<div class="metric-card"><div class="metric-label">{icon} {title}</div><div class="metric-value">{value}</div></div>'
def section_title(text): return f'<div class="section-title">{text}</div>'
def alert_card(text,kind='danger'):
    cls={'danger':'alert-danger','warning':'alert-warning','success':'alert-success'}.get(kind,'alert-danger'); return f'<div class="{cls}">{text}</div>'
def footer(): return '<div class="footer">💊 MediStock — Educational inventory management project only. No medical diagnosis or treatment advice.</div>'
