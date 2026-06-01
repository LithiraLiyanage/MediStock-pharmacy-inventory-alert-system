import pandas as pd, sqlite3
from database.db import execute, fetch_all, fetch_one
from utils.helpers import today_str, add_computed_columns, low_stock_urgency
def get_all_medicines(near_days=30):
    df=pd.DataFrame(fetch_all('SELECT * FROM medicines ORDER BY medicine_name ASC')); return add_computed_columns(df,near_days) if not df.empty else df
def duplicate_exists(medicine_name,batch_number,exclude_id=None):
    row=fetch_one('SELECT id FROM medicines WHERE lower(medicine_name)=lower(?) AND lower(batch_number)=lower(?)'+(' AND id != ?' if exclude_id else ''), (medicine_name,batch_number,exclude_id) if exclude_id else (medicine_name,batch_number)); return row is not None
def add_medicine(data):
    try: return execute("""INSERT INTO medicines(medicine_name,generic_name,category,batch_number,supplier_name,quantity,unit_price,expiry_date,reorder_level,storage_location,notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (data['medicine_name'].strip(),data.get('generic_name','').strip(),data['category'],data['batch_number'].strip(),data.get('supplier_name','').strip(),int(data['quantity']),float(data['unit_price']),str(data['expiry_date']),int(data['reorder_level']),data.get('storage_location','').strip(),data.get('notes','').strip(),today_str(),today_str()))
    except sqlite3.IntegrityError: raise ValueError('Duplicate medicine batch detected.')
def delete_medicine(medicine_id): execute('DELETE FROM stock_movements WHERE medicine_id=?',(medicine_id,)); execute('DELETE FROM medicines WHERE id=?',(medicine_id,))
def get_medicine(medicine_id): return fetch_one('SELECT * FROM medicines WHERE id=?',(medicine_id,))
def filter_medicines(search='',category='All',supplier='All',status='All',near_days=30):
    df=get_all_medicines(near_days)
    if df.empty: return df
    if search: df=df[df['medicine_name'].str.contains(search,case=False,na=False)|df['generic_name'].fillna('').str.contains(search,case=False,na=False)]
    if category!='All': df=df[df['category']==category]
    if supplier!='All': df=df[df['supplier_name']==supplier]
    if status!='All': df=df[df['status']==status]
    return df
def update_stock(medicine_id,movement_type,amount,note=''):
    med=get_medicine(medicine_id)
    if not med: raise ValueError('Medicine not found.')
    prev=int(med['quantity']); amount=int(amount)
    if movement_type=='Stock In': new=prev+amount; change=amount
    elif movement_type=='Stock Out':
        if amount>prev: raise ValueError('Cannot reduce stock below zero.')
        new=prev-amount; change=-amount
    elif movement_type=='Set Exact Stock':
        if amount<0: raise ValueError('Adjustment quantity cannot be negative.')
        new=amount; change=new-prev; movement_type='Adjustment'
    else: raise ValueError('Invalid movement type.')
    execute('UPDATE medicines SET quantity=?, updated_at=? WHERE id=?',(new,today_str(),medicine_id)); execute('INSERT INTO stock_movements(medicine_id,movement_type,quantity_change,previous_quantity,new_quantity,note,created_at) VALUES(?,?,?,?,?,?,?)',(medicine_id,movement_type,change,prev,new,note,today_str())); return new
def get_stock_movements(): return pd.DataFrame(fetch_all('SELECT sm.*, m.medicine_name, m.batch_number FROM stock_movements sm LEFT JOIN medicines m ON m.id=sm.medicine_id ORDER BY sm.created_at DESC'))
def get_expired_medicines(): df=get_all_medicines(); return df if df.empty else df[df['days_remaining']<0].copy()
def get_near_expiry_medicines(days=30): df=get_all_medicines(days); return df if df.empty else df[(df['days_remaining']>=0)&(df['days_remaining']<=days)].copy()
def get_low_stock_medicines():
    df=get_all_medicines()
    if df.empty: return df
    low=df[df['quantity'].astype(int)<=df['reorder_level'].astype(int)].copy()
    if not low.empty: low['urgency']=low.apply(low_stock_urgency,axis=1); low['recommended_reorder_qty']=(low['reorder_level'].astype(int)*2-low['quantity'].astype(int)).clip(lower=1)
    return low
