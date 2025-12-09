import pandas as pd
from sqlalchemy import create_engine, text
import sys

# =======================================================
# 1. KONFIGURASI 
# =======================================================
DB_USER = 'root'
DB_PASSWORD = 'Datarunning.7'  # <-- Password Anda
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'online_retail_db'
CSV_FILE = 'Online Retail.csv'

# =======================================================
# 2. KONEKSI KE DATABASE
# =======================================================
print("🔄 Menghubungkan ke MySQL...")
try:
    connection_str = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_str)
    
    with engine.connect() as conn:
        print(f"✅ Terhubung ke database: {DB_NAME}")
except Exception as e:
    print(f"❌ Gagal koneksi: {e}")
    sys.exit()

# =======================================================
# 3. MEMBERSIHKAN DATA LAMA (RESET)
# =======================================================
print("\n🧹 Membersihkan data lama agar tidak error...")
try:
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("TRUNCATE TABLE Invoice_Details;"))
        conn.execute(text("TRUNCATE TABLE Invoices;"))
        conn.execute(text("TRUNCATE TABLE Products;"))
        conn.execute(text("TRUNCATE TABLE Customers;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        conn.commit()
    print("✨ Database sudah bersih! Siap diisi ulang.")
except Exception as e:
    print(f"⚠️ Peringatan saat reset: {e}")

# =======================================================
# 4. MEMBACA & MEMPROSES DATA
# =======================================================
print(f"\n📖 Membaca file CSV: {CSV_FILE} ...")
try:
    df = pd.read_csv(
        CSV_FILE, 
        encoding='latin1',
        parse_dates=['InvoiceDate'],
        dtype={'InvoiceNo': str, 'StockCode': str, 'CustomerID': str}
    )
    df.dropna(subset=['StockCode'], inplace=True)
    
    # --- PERBAIKAN UTAMA DI SINI ---
    # Ubah semua StockCode jadi HURUF BESAR dan String
    # Ini mengatasi error Duplicate entry '15056bl' vs '15056BL'
    df['StockCode'] = df['StockCode'].astype(str).str.strip().str.upper()
    
    print(f"   -> Total baris data: {len(df)}")
except Exception as e:
    print(f"❌ Error membaca CSV: {e}")
    sys.exit()

def upload_table(dataframe, table_name, chunk_size=10000):
    print(f"🚀 Mengupload ke '{table_name}' ({len(dataframe)} baris)...")
    try:
        dataframe.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=True,
            chunksize=chunk_size
        )
        print(f"✅ Sukses: {table_name}")
    except Exception as e:
        print(f"❌ GAGAL {table_name}: {e}")
        if table_name in ['Customers', 'Products']:
            print("🛑 Program dihentikan karena tabel induk gagal.")
            sys.exit()

# --- A. CUSTOMERS ---
customers = df[['CustomerID', 'Country']].dropna(subset=['CustomerID']).drop_duplicates(subset=['CustomerID']).copy()
customers['CustomerID'] = customers['CustomerID'].astype(int)
customers.set_index('CustomerID', inplace=True)
upload_table(customers, 'Customers')

# --- B. PRODUCTS ---
# Karena StockCode sudah di-UPPERCASE di atas, drop_duplicates sekarang akan bekerja sempurna
products = df[['StockCode', 'Description']].drop_duplicates(subset=['StockCode']).copy()
products.set_index('StockCode', inplace=True)
upload_table(products, 'Products')

# --- C. INVOICES ---
invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo']).copy()
invoices['CustomerID'] = pd.to_numeric(invoices['CustomerID'], errors='coerce').astype('Int64')
invoices.set_index('InvoiceNo', inplace=True)
upload_table(invoices, 'Invoices')

# --- D. INVOICE_DETAILS ---
details = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']].copy()
details.reset_index(drop=True, inplace=True)
details.index = details.index + 1 
details.index.name = 'DetailID'
upload_table(details, 'Invoice_Details')

print("\n🎉 SELESAI! SEMUA DATA BERHASIL DIIMPOR.")