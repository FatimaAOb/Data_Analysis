# E-commerce Customer Behavior Analysis

## Project Overview
Analysis of online retail transactions to identify customer segments, product performance, and revenue trends to support marketing and inventory decisions.

## Business Questions
1. What are our revenue trends and seasonality patterns?
2. Who are our most valuable customers?
3. Which products drive the most revenue?
4. What is our customer retention status?

## Data Source
- Dataset: UCI Online Retail Dataset
- Period: 2010-2011
- Records: 540,000+ transactions
- Geography: Primarily UK

## Tools Used
- SQL Server Management Studio - Data profiling and analysis
- Python (pandas, matplotlib, seaborn) - Data cleaning and visualization
- Power BI - Interactive dashboard

## Data Cleaning Steps
1. Removed 135,000 rows with missing CustomerID (25% of data)
2. Filtered out 10,000 return transactions (negative quantities)
3. Removed 2 rows with negative unit prices
4. Created calculated field: TotalPrice = Quantity × UnitPrice
5. Extracted date components for time-series analysis

**Rationale:** CustomerID is essential for customer behavior analysis. Returns require separate analysis.

## Key Findings
1. **Revenue Growth:** 
2. **Customer Segmentation:** 

3. **Top Products:** "Regency Cakestand 3 tier" generated £ (3.5% of total revenue)
4. **Geographic Insights:** 

## Recommendations
1. Implement win-back campaign for churned customers
2. Increase inventory for top 20 products
3. Investigate low retention rates (% churn)
4. Expand marketing in high-performing countries

## How to Reproduce
1. Download dataset, availabe in folder.
2. Import to SQL Server using provided scripts
3. Run Python cleaning script
4. Execute SQL analysis queries
5. Open Power BI dashboard


