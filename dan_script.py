import pandas as pd
import matplotlib.pyplot as plt

""" df = pd.read_csv("./MELBOURNE_HOUSE_PRICES_LESS.csv")

# Dropping rows that has null cells in Price
df.dropna(subset=["Price"], inplace=True)

# Align date format
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

df["Price"] = df["Price"].astype(int)

# print(df)

# Drop unecessary columns
df.drop(columns=["Method", "SellerG"], axis=1, inplace=True)

# Cleaned dataset
# df.to_csv("out.csv", index=False)

mean_prices_by_council = df.groupby("CouncilArea")["Price"].mean() / 1_000_000

plt.figure(figsize=(10, 6))
mean_prices_by_council.plot(kind='bar')
plt.ylabel("Mean Price (in $1,000,000)")
plt.title("Mean House Prices by Council Area")
plt.xticks(rotation=45, ha="right")
plt.show() """

df1 = pd.read_csv("./median-house-prices-by-type-and-sale-year.csv")

df1 = df1[df1["type"] == "House/Townhouse"].sort_values(by="sale_year")

df1.reset_index(drop=True, inplace=True)

df1.drop(columns=["type", "transaction_count"], axis=1, inplace=True)

# print(df1)

min_year = df1["sale_year"].min()
max_year = df1["sale_year"].max()

plt.figure(figsize=(10, 6))
plt.plot(df1["sale_year"], df1["median_price"], marker="o", linestyle="-", color="b")
plt.ylim(bottom=0)
plt.xlim(min_year, max_year)
plt.xticks(range(min_year, max_year + 1, 1))
plt.xlabel("Year")
plt.ylabel("Median House Price")
plt.title("Median House/Townhouse Prices by Sale Year")
plt.grid(True)
plt.show()