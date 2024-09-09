import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
import numpy as np

def main():
    # func1()
    # func2()
    # func3()
    func4()

def func1():
    df = pd.read_csv("./MELBOURNE_HOUSE_PRICES_LESS.csv")

    # Dropping rows that has null cells in Price
    df.dropna(subset=["Price"], inplace=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    df["Price"] = df["Price"].astype(int) / 1_000_000

    # print(df)

    # Drop unecessary columns
    # df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Date"], axis=1, inplace=True)

    """ # Cleaned dataset
    # df.to_csv("out.csv", index=False)

    mean_prices_by_council = df.groupby("CouncilArea")["Price"].mean() / 1_000_000

    plt.figure(figsize=(10, 6))
    mean_prices_by_council.plot(kind='bar')
    plt.ylabel("Mean Price (in $1,000,000)")
    plt.title("Mean House Prices by Council Area")
    plt.xticks(rotation=45, ha="right")
    plt.show() """

    x = df[["Price"]]
    y = df["Distance"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    # Print model performance
    print('Mean Squared Error: %.2f' % mean_squared_error(y_test, y_pred))
    print('R^2 Score: %.2f' % r2_score(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_test, y_test, color='black', label='Actual values')
    plt.plot(x_test, y_pred, color='blue', linewidth=3, label='Predicted values')
    plt.xlabel('Distance')
    plt.ylabel('Price')
    plt.title('Linear Regression on Melbourne Housing Dataset')
    plt.legend()
    plt.show()

def func2():
    df = pd.read_csv("./median-house-prices-by-type-and-sale-year.csv")

    # df = df[df["type"] == "House/Townhouse"].sort_values(by="sale_year")
    df = df[df["type"] == "Residential Apartment"].sort_values(by="sale_year")

    df["median_price"] = df["median_price"].astype(int) / 100_000

    df.reset_index(drop=True, inplace=True)

    """ # Visualise initial dataset 
    df.drop(columns=["type", "transaction_count"], axis=1, inplace=True)

    # print(df)

    min_year = df["sale_year"].min()
    max_year = df["sale_year"].max()

    plt.figure(figsize=(10, 6))
    plt.plot(df["sale_year"], df["median_price"], marker="o", linestyle="-", color="b")
    plt.ylim(bottom=0)
    plt.xlim(min_year, max_year)
    plt.xticks(range(min_year, max_year + 1, 1))
    plt.xlabel("Year")
    plt.ylabel("Median House Price")
    plt.title("Median House/Townhouse Prices by Sale Year")
    plt.grid(True)
    plt.show() """

    # Build model
    x = df[["sale_year"]]
    y = df["median_price"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    # Print model performance
    print('Mean Squared Error: %.2f' % mean_squared_error(y_test, y_pred))
    print('R^2 Score: %.2f' % r2_score(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_test, y_test, color='black', label='Actual values')
    plt.plot(x_test, y_pred, color='blue', linewidth=3, label='Predicted values')
    plt.xlabel('sale_year')
    plt.ylabel('median_price')
    plt.title('Linear Regression on Melbourne Housing Dataset')
    plt.legend()
    plt.show()

def func3():
    df = pd.read_csv("./Australian Bureau of Statistics.csv", skiprows=1)

    df1 = df.drop(df.index[[1, 2, 3, 4, -1]]).reset_index(drop=True)

    df1.rename(columns={df1.columns[0]: "Year"}, inplace=True)

    # Remove quotation marks and commas in numeric values, convert them to float
    df1.iloc[:, 1:] = df1.iloc[:, 1:].replace('[\$,]', '', regex=True).astype(float)

    # Create a new DataFrame to store Year and Average Income
    avg_df = pd.DataFrame(columns=["Year", "Income"])

    print(df1)

    data = []

    # Loop over the DataFrame to calculate the averages between consecutive years
    for i in range(len(df1.columns) - 2):
        year = int(df1.columns[i + 1].split('-')[1]) + 2000 # Extract the end year
        avg_income = (df1.iloc[0, i + 1] + df1.iloc[0, i + 2]) / 2  # Calculate the average
        data.append({"Year": year, "Income": avg_income})

    avg_df = pd.DataFrame(data)

    avg_df['Year'] = avg_df['Year'].astype(int)

    # Print the resulting DataFrame
    print(avg_df)

    avg_df.to_csv("out.csv", index=False)

def func4():
    data = []

    # income: equivalised disposable household income per week

    data.append({"Year": "1999-00", "Median Income": None})

    df = pd.read_excel("./65230_complete_set.xls", sheet_name="Table 12 Cap city")
    income = df.iloc[11, 7] * 52
    data.append({"Year": "2000-01", "Median Income": income})

    data.append({"Year": "2001-02", "Median Income": None})

    df = pd.read_excel("./6523.0_datacube_2002-03.xls", sheet_name="Table 13A")
    income = df.iloc[12, 8] * 52
    data.append({"Year": "2002-03", "Median Income": income})

    df = pd.read_excel("./65230_data_2003-04.xls", sheet_name="Table 14")
    income = df.iloc[12, 6] * 52
    data.append({"Year": "2003-04", "Median Income": income})

    data.append({"Year": "2004-05", "Median Income": None})

    df = pd.read_excel("./65230DO001_200506.XLS", sheet_name="Table 14")
    income = df.iloc[13, 3] * 52
    data.append({"Year": "2005-06", "Median Income": income})

    data.append({"Year": "2006-07", "Median Income": None})

    df = pd.read_excel("./65230do001_200708.xls", sheet_name="Table_14")
    income = df.iloc[11, 3] * 52
    data.append({"Year": "2007-08", "Median Income": income})

    data.append({"Year": "2008-09", "Median Income": None})

    df = pd.read_excel("./65230do001_200910.xls", sheet_name="Table_15")
    income = df.iloc[11, 3] * 52
    data.append({"Year": "2009-10", "Median Income": income})

    data.append({"Year": "2010-11", "Median Income": None})

    df = pd.read_excel("./6124055002ds0001_2019.xls", sheet_name="Table 1.1")
    income = df.iloc[11, 20]
    data.append({"Year": "2011-12", "Median Income": income})
    
    income = df.iloc[11, 21]
    data.append({"Year": "2012-13", "Median Income": income})
    
    income = df.iloc[11, 22]
    data.append({"Year": "2013-14", "Median Income": income})
    
    income = df.iloc[11, 23]
    data.append({"Year": "2014-15", "Median Income": income})
    
    income = df.iloc[11, 24]
    data.append({"Year": "2015-16", "Median Income": income})
    
    income = df.iloc[11, 25]
    data.append({"Year": "2016-17", "Median Income": income})

    df = pd.DataFrame(data)

    print(df)


if __name__ == "__main__":
    main()