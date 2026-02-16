import pandas as pd


#Load data
onlineRetaildata=pd.read_csv("Online_Retail.csv")
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
#Data info
print(f"Initial Shape: {onlineRetaildata.shape}")
print(f"Missing values: \n {onlineRetaildata.isnull().sum()}")
print(f"Data types: \n {onlineRetaildata.dtypes}")

#Clean data
#1. Remove rows with missing CustomerID (can't analyze customer behavior)
onlineRetaildata_clean=onlineRetaildata.dropna(subset=["CustomerID"]).copy()

#2. Handle negative quantities
onlineRetaildata_clean["is_returned"]=onlineRetaildata_clean["Quantity"]<=0
onlineRetaildata_clean=onlineRetaildata_clean.loc[onlineRetaildata_clean["Quantity"]>0] #only analyze complete purchases

#3 Remove negative prices
onlineRetaildata_clean=onlineRetaildata_clean.loc[onlineRetaildata_clean["UnitPrice"]>0]

#4 Create calcualted fields
onlineRetaildata_clean["TotalPrice"]=onlineRetaildata_clean["UnitPrice"]*onlineRetaildata_clean["Quantity"]
onlineRetaildata_clean["InvoiceDate"]=pd.to_datetime(onlineRetaildata_clean["InvoiceDate"], format="mixed")
onlineRetaildata_clean["Year"]=onlineRetaildata_clean["InvoiceDate"].dt.year
onlineRetaildata_clean["Month"]=onlineRetaildata_clean["InvoiceDate"].dt.month
onlineRetaildata_clean["DayOfWeek"]=onlineRetaildata_clean["InvoiceDate"].dt.day_name()

#5 Handle duplicates
duplicates=onlineRetaildata_clean.duplicated().sum() #5192

if duplicates>0:
    onlineRetaildata_clean=onlineRetaildata_clean.drop_duplicates()
    print(f"removed {duplicates} duplicate rows")

#onlineRetaildata_clean.to_csv("onlineRetailData.csv", index=False)