--1 dataset info
EXEC sp_help "Online_Retail"
EXEC sp_spaceused


--2 Initial exploration
--query results: total rows: 541909, unique invoices: 25900, unique customers: 4372
SELECT COUNT(*) as total_rows, 
	COUNT(DISTINCT InvoiceNo) as unique_invoices,
	COUNT(DISTINCT CustomerID) as unique_customers
FROM Online_Retail

--3 Missing values analysis
--Description has 1454 (0.2%),  customerID has 135080 (24.9%) missing values 
SELECT COUNT(*) as total_rows, 
SUM(CASE WHEN InvoiceNo IS NULL THEN 1 ELSE 0 END) as missing_invoiceNo,
SUM(CASE WHEN StockCode IS NULL THEN 1 ELSE 0 END) as missing_stockcode,
SUM(CASE WHEN Description IS NULL THEN 1 ELSE 0 END) as missing_description,
SUM (CASE WHEN Quantity IS NULL THEN 1 ELSE 0 END) as missing_quantity,
SUM (CASE WHEN InvoiceDate IS NULL THEN 1 ELSE 0 END) as missing_invoucedate,
SUM (CASE WHEN UnitPrice IS NULL THEN 1 ELSE 0 END) as missing_unitprice,
SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) as missing_customerID,
SUM (CASE WHEN Country IS NULL THEN 1 ELSE 0 END) as missing_country
FROM Online_Retail

--4 Data quality issues
--10624 rows with quantity<0 which means cancellation or returns, 0s are data errors, 2517 with unitprice<=0 (errors)
SELECT * 
FROM Online_Retail
WHERE Quantity <= 0 

SELECT *
FROM Online_Retail
WHERE UnitPrice <= 0

--check if anything needs trimming
SELECT *
FROM Online_Retail
WHERE InvoiceDate LIKE ' %' OR InvoiceDate LIKE '% '
SELECT *
FROM Online_Retail
WHERE InvoiceNo LIKE ' %' OR InvoiceNo LIKE '% ' 
SELECT *
FROM Online_Retail
WHERE StockCode LIKE ' %' OR StockCode LIKE '% '
--DESCRIPTION has 112626 rows with trimming needed.
SELECT *
FROM Online_Retail
WHERE Description LIKE ' %' OR Description LIKE '% '
SELECT *
FROM Online_Retail
WHERE Quantity LIKE ' %' OR Quantity LIKE '% '
SELECT *
FROM Online_Retail
WHERE UnitPrice LIKE ' %' OR UnitPrice LIKE '% '
SELECT *
FROM Online_Retail
WHERE CustomerID LIKE ' %' OR CustomerID LIKE '% '
SELECT *
FROM Online_Retail
WHERE Country LIKE ' %' OR Country LIKE '% ' 


--5 timeline analysis
--2010-12-01 08:26:00.0000000 to 2011-12-09 12:50:00.0000000
SELECT MIN(InvoiceDate) as earliestOrder, MAX(InvoiceDate) as latestOrder
FROM Online_Retail
	


