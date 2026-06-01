import plotly.express as px
from services.inventory_service import get_all_medicines, get_low_stock_medicines, get_expired_medicines, get_near_expiry_medicines
def dashboard_metrics():
    df=get_all_medicines()
    if df.empty: return dict(total_medicines=0,total_quantity=0,inventory_value=0,low_stock_count=0,out_of_stock_count=0,expired_count=0,near_expiry_count=0,categories_count=0)
    return dict(total_medicines=len(df),total_quantity=int(df['quantity'].sum()),inventory_value=float(df['stock_value'].sum()),low_stock_count=len(get_low_stock_medicines()),out_of_stock_count=int((df['quantity']<=0).sum()),expired_count=len(get_expired_medicines()),near_expiry_count=len(get_near_expiry_medicines(30)),categories_count=df['category'].nunique())
def category_chart(df): return None if df.empty else px.bar(df.groupby('category',as_index=False)['quantity'].sum(),x='category',y='quantity',title='Medicines by Category',color='category')
def value_chart(df): return None if df.empty else px.bar(df.groupby('category',as_index=False)['stock_value'].sum(),x='category',y='stock_value',title='Inventory Value by Category',color='category')
def expiry_pie(df):
    if df.empty: return None
    data=df['status'].value_counts().reset_index(); data.columns=['status','count']; return px.pie(data,names='status',values='count',title='Expiry / Stock Status Distribution')
def low_stock_urgency_chart(low_df):
    if low_df.empty or 'urgency' not in low_df.columns: return None
    data=low_df['urgency'].value_counts().reset_index(); data.columns=['urgency','count']; return px.bar(data,x='urgency',y='count',title='Low Stock Urgency',color='urgency')
def monthly_expiry_chart(df):
    if df.empty: return None
    pd=__import__('pandas'); temp=df.copy(); temp['expiry_month']=pd.to_datetime(temp['expiry_date']).dt.to_period('M').astype(str); data=temp.groupby('expiry_month',as_index=False)['id'].count(); data.columns=['expiry_month','medicine_count']; return px.line(data,x='expiry_month',y='medicine_count',markers=True,title='Monthly Expiry Distribution')
