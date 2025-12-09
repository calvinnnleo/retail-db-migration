USE online_retail_db;

SELECT * FROM Customers LIMIT 10;

SELECT * FROM Products LIMIT 10;

SELECT COUNT(*) FROM Invoice_Details;

SELECT 
    p.Description, 
    SUM(d.Quantity) as Total_Terjual
FROM Invoice_Details d
JOIN Products p ON d.StockCode = p.StockCode
GROUP BY p.Description
ORDER BY Total_Terjual DESC
LIMIT 5;

SELECT 
    c.Country, 
    COUNT(DISTINCT i.InvoiceNo) as Jumlah_Transaksi
FROM Invoices i
JOIN Customers c ON i.CustomerID = c.CustomerID
GROUP BY c.Country
ORDER BY Jumlah_Transaksi DESC
LIMIT 5;

SELECT 
    c.CustomerID,
    SUM(d.Quantity * d.UnitPrice) as Total_Belanja
FROM Invoices i
JOIN Invoice_Details d ON i.InvoiceNo = d.InvoiceNo
JOIN Customers c ON i.CustomerID = c.CustomerID
GROUP BY c.CustomerID
ORDER BY Total_Belanja DESC
LIMIT 5;