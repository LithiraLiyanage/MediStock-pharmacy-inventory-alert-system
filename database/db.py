import sqlite3
from pathlib import Path
from datetime import date, timedelta
from utils.helpers import today_str
DB_PATH=Path('data/medistock.db')
def get_connection():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True); conn=sqlite3.connect(DB_PATH); conn.row_factory=sqlite3.Row; return conn
def execute(query,params=()):
    with get_connection() as conn: cur=conn.cursor(); cur.execute(query,params); conn.commit(); return cur.lastrowid
def fetch_all(query,params=()):
    with get_connection() as conn: cur=conn.cursor(); cur.execute(query,params); return [dict(r) for r in cur.fetchall()]
def fetch_one(query,params=()):
    with get_connection() as conn: cur=conn.cursor(); cur.execute(query,params); row=cur.fetchone(); return dict(row) if row else None
def init_db():
    execute("""CREATE TABLE IF NOT EXISTS medicines(id INTEGER PRIMARY KEY AUTOINCREMENT,medicine_name TEXT NOT NULL,generic_name TEXT,category TEXT NOT NULL,batch_number TEXT NOT NULL,supplier_name TEXT,quantity INTEGER NOT NULL,unit_price REAL NOT NULL,expiry_date TEXT NOT NULL,reorder_level INTEGER NOT NULL,storage_location TEXT,notes TEXT,created_at TEXT,updated_at TEXT,UNIQUE(medicine_name,batch_number))""")
    execute("""CREATE TABLE IF NOT EXISTS stock_movements(id INTEGER PRIMARY KEY AUTOINCREMENT,medicine_id INTEGER,movement_type TEXT,quantity_change INTEGER,previous_quantity INTEGER,new_quantity INTEGER,note TEXT,created_at TEXT,FOREIGN KEY(medicine_id) REFERENCES medicines(id))""")
    seed_demo_data()
def seed_demo_data():
    row=fetch_one('SELECT COUNT(*) AS total FROM medicines')
    if row and row['total']>0: return
    today=date.today(); demo=[('Paracetamol','Acetaminophen','Pain Relief','PCM-001','HealthPlus',8,12.5,today+timedelta(days=200),20,'A1','Low stock demo'),('Amoxicillin','Amoxicillin','Antibiotic','AMX-112','MediSupply',45,28,today+timedelta(days=15),15,'B2','Near expiry demo'),('Cetirizine','Cetirizine','Allergy','CTZ-211','AllergyCare',0,9.5,today+timedelta(days=300),10,'A3','Out of stock demo'),('Metformin','Metformin','Diabetes','MET-520','DiabeCare',130,18.75,today+timedelta(days=420),30,'C1',''),('Amlodipine','Amlodipine','Blood Pressure','AML-890','CardioMed',75,22,today+timedelta(days=90),25,'C2',''),('Vitamin C','Ascorbic Acid','Vitamins','VTC-330','VitaLife',210,6.5,today+timedelta(days=700),50,'D1',''),('Omeprazole','Omeprazole','Digestive Health','OMP-451','GastroPharm',16,14,today+timedelta(days=6),20,'D3','Urgent expiry demo'),('Ibuprofen','Ibuprofen','Pain Relief','IBU-221','ReliefCo',60,16.25,today-timedelta(days=5),20,'A2','Expired demo'),('Saline Solution','Sodium Chloride','First Aid','SAL-099','CareFirst',34,35,today+timedelta(days=150),12,'E1',''),('Cough Syrup','Dextromethorphan','Cold & Flu','CS-762','ColdCare',18,42,today+timedelta(days=25),18,'F2','Near reorder demo')]
    for item in demo: execute("""INSERT INTO medicines(medicine_name,generic_name,category,batch_number,supplier_name,quantity,unit_price,expiry_date,reorder_level,storage_location,notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (*item[:7],item[7].strftime('%Y-%m-%d'),*item[8:],today_str(),today_str()))
