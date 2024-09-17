import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

sys.path.append('../')
import data_functions


#Plot future house prices based on crime data
def plot_future_prices(df):
    #plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x/1e6), '.1f') + 'M'))
    df_pivot = df.pivot_table(index='Year', columns='CouncilArea', values='Price')
    df_pivot.plot(kind='line', marker='o', figsize=(12, 8))
    plt.title('Price Trend by Council Area')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

#Plots Crime Data
def plot_crime_data(df):
    #Initialise Matplotlib
    plt.figure(figsize=(25, 15))
    plt.style.use('seaborn-v0_8-darkgrid')

    # Get all the councils
    councils = df["CouncilArea"].unique()
    # Colors for each council
    colors = plt.cm.get_cmap('hsv', len(councils))

    #plot each council
    for index, council in enumerate(councils):
        council_data = df[df["CouncilArea"] == council]
        plt.plot(council_data["Year"], council_data["Yearly Rate per 100,000 population"],
                label=council, color=colors(index))

    # Add title and labels
    plt.title("Crime Rate per 100,000 Population Across Greater Melbourne Councils (Yearly Data)", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Crime Rate per 100,000 Population", fontsize=12)
    plt.xticks(rotation=45)

    #Legend, Tight layout and showing the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.show()

def main():
    data_functions.clean_house_price_data().to_csv("house.csv", index=False)
    HousingCrimeDF = data_functions.merge_all_data()
    HousingCrimeDF.to_csv("all_data.csv", index=False)
    predictedFuturePrices = use_polynomial_regression_to_predict_house_price(HousingCrimeDF)
    combinedHousingPriceData = combine_predictions_with_actual(HousingCrimeDF, predictedFuturePrices)
    combinedHousingPriceData.to_csv("out_predictions.csv", index=False)
    plot_future_prices(combinedHousingPriceData)

if __name__ == "__main__":
    main()