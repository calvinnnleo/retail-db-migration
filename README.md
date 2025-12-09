# Online Retail Database

Sistem database MySQL untuk analisis penjualan retail online dengan import otomatis dari CSV menggunakan Python.

## Struktur Database

- **Customers** - Data pelanggan (CustomerID, Country)
- **Products** - Data produk (StockCode, Description)
- **Invoices** - Data invoice (InvoiceNo, InvoiceDate, CustomerID)
- **Invoice_Details** - Detail transaksi (DetailID, InvoiceNo, StockCode, Quantity, UnitPrice)

## Instalasi

```bash
# Install dependencies
pip install pandas sqlalchemy pymysql

# Buat database
CREATE DATABASE online_retail_db;
```

Edit kredensial di `import_data.py`:
```python
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
```

## Penggunaan

```bash
# Import data dari CSV
python import_data.py

# Jalankan query analisis
mysql -u root -p online_retail_db < db_online.retail.sql
```

## Query Contoh

**Top 5 Produk Terlaris:**
```sql
SELECT p.Description, SUM(d.Quantity) as Total_Terjual
FROM Invoice_Details d
JOIN Products p ON d.StockCode = p.StockCode
GROUP BY p.Description
ORDER BY Total_Terjual DESC LIMIT 5;
```

**Top 5 Negara:**
```sql
SELECT c.Country, COUNT(DISTINCT i.InvoiceNo) as Jumlah_Transaksi
FROM Invoices i
JOIN Customers c ON i.CustomerID = c.CustomerID
GROUP BY c.Country
ORDER BY Jumlah_Transaksi DESC LIMIT 5;
```

## Fitur

- Otomatis cleaning data (normalisasi StockCode ke UPPERCASE)
- Menangani duplikasi
- Batch processing untuk efisiensi
- Reset database otomatis sebelum import

## Troubleshooting

- **Connection refused**: Pastikan MySQL service running
- **File not found**: Letakkan `Online Retail.csv` di folder yang sama
- **Duplicate entry**: Script otomatis menangani dengan normalisasi data
