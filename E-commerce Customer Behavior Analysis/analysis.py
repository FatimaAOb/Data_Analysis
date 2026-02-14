import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

onlineretaildf=pd.read_csv("onlineRetailData.csv")
onlineretaildf['InvoiceDate']=pd.to_datetime(onlineretaildf['InvoiceDate'])

#1 Revenue trend over time
monthly_revenue=onlineretaildf.groupby(onlineretaildf['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
plt.figure(figsize=(12,6))
monthly_revenue.plot(kind='line')
plt.title("Monthly revenue trend")
plt.xlabel("Month")
plt.ylabel("Revene")
plt.tight_layout()
#plt.show()
plt.savefig("Monthly_Revenue_Trend.png", dpi=300)

#2 Customer distribution by total spend
customer_spend=onlineretaildf.groupby('CustomerID')['TotalPrice'].sum()
plt.figure(figsize=(10,6))
plt.hist(customer_spend, bins=50, edgecolor='black')
plt.title("Customer Spend Distribution")
plt.xlabel("Total Spend")
plt.ylabel("Number of customers")
#plt.xlim(0,20000)
plt.tight_layout()
#plt.show()
plt.savefig("Customer_Spend_Distribution.png", dpi=300)

#3 Top 10 products
top_products=onlineretaildf.groupby('Description')['TotalPrice'].sum().nlargest(10)
plt.figure(figsize=(12,6))
top_products.plot(kind='barh')
plt.title("Top 10 products")
plt.xlabel("Revenue")
plt.tight_layout()
#plt.show()
plt.savefig("Top_10_Products.png", dpi=300)