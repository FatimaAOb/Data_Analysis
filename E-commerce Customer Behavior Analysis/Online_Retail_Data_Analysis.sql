-- 1. Monthly revenue trends
SELECT 
    YEAR(InvoiceDate) as Year,
    MONTH(InvoiceDate) as Month,
    COUNT(DISTINCT CustomerID) as unique_customers,
    COUNT(DISTINCT InvoiceNo) as total_orders,
    SUM(Quantity * UnitPrice) as total_revenue
FROM onlineRetailData
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY Year, Month;

-- 2. Customer segmentation (RFM Analysis)
WITH customer_metrics AS (
    SELECT 
        CustomerID,
        MAX(InvoiceDate) as recency,
        COUNT(DISTINCT InvoiceNo) as frequency,
        SUM(Quantity * UnitPrice) as monetary
    FROM onlineRetailData
    GROUP BY CustomerID
)
SELECT 
    CustomerID,
    DATEDIFF(day, recency, '2011-12-31') as recency_days,
    frequency,
    monetary,
   CASE 
    WHEN DATEDIFF(day, recency, '2011-12-31') <=30 AND frequency>=5 AND monetary >=1000 THEN 'ACTIVE, LOYAL' 
    WHEN DATEDIFF(day, recency, '2011-12-31')<=90 THEN 'AT RISK' 
    WHEN DATEDIFF(day, recency, '2011-12-31')>=90 AND frequency>=10 AND monetary >=100 THEN 'High value, Re-engagment needed' 
   ELSE 'CHURNED' END AS customer_status
FROM customer_metrics;

-- 3. Product performance
SELECT TOP 20
    Description,
    COUNT(DISTINCT InvoiceNo) as times_purchased,
    SUM(Quantity) as total_quantity,
    SUM(Quantity * UnitPrice) as total_revenue
FROM onlineRetailData
GROUP BY Description
ORDER BY total_revenue DESC;