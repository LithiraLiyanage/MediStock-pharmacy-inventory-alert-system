from datetime import date, datetime

def today_str(): return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def parse_date(value):
    if isinstance(value, date): return value
    return datetime.strptime(str(value), '%Y-%m-%d').date()
def days_until(expiry_date):
    try: return (parse_date(expiry_date) - date.today()).days
    except Exception: return None
def money(value):
    try: return f'LKR {float(value):,.2f}'
    except Exception: return 'LKR 0.00'
def medicine_status(row, near_days=30):
    qty=int(row.get('quantity',0)); reorder=int(row.get('reorder_level',0)); days=days_until(row.get('expiry_date'))
    if days is not None and days < 0: return 'Expired'
    if qty <= 0: return 'Out of Stock'
    if days is not None and days <= near_days: return 'Near Expiry'
    if qty <= reorder: return 'Low Stock'
    return 'In Stock'
def add_computed_columns(df, near_days=30):
    if df.empty: return df
    df=df.copy(); df['days_remaining']=df['expiry_date'].apply(days_until); df['stock_value']=df['quantity'].astype(float)*df['unit_price'].astype(float); df['status']=df.apply(lambda r: medicine_status(r, near_days), axis=1); return df
def low_stock_urgency(row):
    qty=int(row.get('quantity',0)); reorder=int(row.get('reorder_level',0))
    if qty <= 0: return 'Critical'
    if reorder > 0 and qty < reorder * 0.5: return 'High'
    return 'Medium'
def readable_table(df):
    if df.empty: return df
    d=df.copy()
    if 'stock_value' in d.columns: d['stock_value']=d['stock_value'].apply(money)
    return d
