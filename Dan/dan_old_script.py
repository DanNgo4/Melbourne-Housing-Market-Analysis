import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def main():
    data = fetch_data()
    df = transform_data(data) 
    train_model(df)

def fetch_data():
    data = []

    # income: equivalised disposable household income per week

    df = pd.read_excel("./Dan/65230_complete_set.xls", sheet_name="Table 12 Cap city")
    income = prev = df.iloc[11, 7] * 52
    data.append({"Year": "2000-01", "Median Income": income})

    df = pd.read_excel("./Dan/6523.0_datacube_2002-03.xls", sheet_name="Table 13A")
    income = next = df.iloc[12, 8] * 52
    data.append({"Year": "2002-03", "Median Income": income})

    data.append({"Year": "2001-02", "Median Income": int((prev + next) / 2)})


    df = pd.read_excel("./Dan/65230_data_2003-04.xls", sheet_name="Table 14")
    income = prev = df.iloc[12, 6] * 52
    data.append({"Year": "2003-04", "Median Income": income})

    df = pd.read_excel("./Dan/65230DO001_200506.XLS", sheet_name="Table 14")
    income = next = df.iloc[13, 3] * 52
    data.append({"Year": "2005-06", "Median Income": income})

    data.append({"Year": "2004-05", "Median Income": int((prev + next) / 2)})


    prev = next # income 05-06

    df = pd.read_excel("./Dan/65230do001_200708.xls", sheet_name="Table_14")
    income = next = df.iloc[11, 3] * 52
    data.append({"Year": "2007-08", "Median Income": income})

    data.append({"Year": "2006-07", "Median Income": int((prev + next) / 2)})


    prev = next # income 07-08

    df = pd.read_excel("./Dan/65230do001_200910.xls", sheet_name="Table_15")
    income = next = df.iloc[11, 3] * 52
    data.append({"Year": "2009-10", "Median Income": income})

    data.append({"Year": "2008-09", "Median Income": int((prev + next) / 2)})


    prev = next # income 09-10

    df = pd.read_excel("./Dan/6124055002ds0001_2019.xls", sheet_name="Table 1.1")
    income = next = df.iloc[11, 20]
    data.append({"Year": "2011-12", "Median Income": income})
    
    data.append({"Year": "2010-11", "Median Income": int(prev + next) / 2})


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

    data.append({"Year": "1999-00", "Median Income": None})

    data = sorted(data, key=lambda x: x["Year"])

    return data


def transform_data(data):
    start_value = data[1]["Median Income"]
    end_value = data[-1]["Median Income"]
    n_years = 2016 - 2000 # num of years between 2000-01 and 2016-17

    cagr = ((end_value / start_value) ** (1 / n_years)) - 1

    income = start_value / (1 + cagr)
    data[0]["Median Income"] = int(income)

    data1 = []
    for i in range(len(data) - 1):
        year = int(data[i]["Year"].split("-")[1]) + 2000
        income = int((data[i]["Median Income"] + data[i + 1]["Median Income"]) / 2)
        data1.append({"Year": year, "Median Income": income})

    df = pd.DataFrame(data1)

    df1 = pd.read_csv("./Dan/median-house-prices-by-type-and-sale-year.csv")

    #df1 = df1.sort_values(by=["sale_year", "type"])

    #df1.reset_index(drop=True, inplace=True)

    df1.drop(columns="transaction_count", axis=1, inplace=True)

    df1 = df1.groupby('sale_year', as_index=False).agg({'median_price': 'mean'})
    df1["median_price"] = df1["median_price"].astype(int)

    df_merged = pd.merge(df, df1, left_on='Year', right_on='sale_year')

    df_merged = df_merged.drop(columns=['sale_year'])

    return df_merged


def train_model(df_merged):
    x = df_merged[["median_price"]]
    y = df_merged["Median Income"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_test, y_test, color="black", label="Actual Values")
    plt.plot(x_test, y_pred, color="blue", linewidth=3, label="Predicted Values")
    plt.xlabel("Price")
    plt.ylabel("Income")
    plt.title("Linear Regression on Melbourne Housing Dataset")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()