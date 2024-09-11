import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

GreaterMelbourneLGAs=["Bayside City Council","Merri-bek City Council","Melbourne City Council","Kingston City Council","Greater Dandenong City Council",
                      "Frankston City Council","Glen Eira City Council","Monash City Council","Stonnington City Council","Port Phillip City Council",
                      "Yarra City Council","Casey City Council","Wyndham City Council","Whittlesea City Council","Nillumbik City Council",
                      "Melton City Council","Moonee Valley City Council","Maribyrnong City Council","Hume City Council","Hobsons Bay City Council",
                      "Darebin City Council","Knox City Council","Brimbank City Council","Banyule City Council","Cardinia City Council","MaroondahCity Council",
                      "Manningham City Council","Boroondara City Council"]

futureCrime={}


#Cleans the Data and manipulates crime data
def clean_and_manipulate_crime_data():

    df = pd.read_csv("./Mitchell/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

    #Remove Police Region, Not applicable for model
    df.drop(columns="Police Region", axis=1, inplace=True)

    #Remove whitespaces on LGA's
    df['Local Government Area'] = df['Local Government Area'].str.strip()

    #Append " City Council" to end to match LGA column in Housing price dataset
    df['Local Government Area'] = df['Local Government Area'] + " City Council"

    #Drop any LGA's not in Greater Melbourne
    df.drop(df[~df['Local Government Area'].isin(GreaterMelbourneLGAs)].index, inplace = True)

    #Convert Crimes in LGA to int
    df['Incidents Recorded'] = df['Incidents Recorded'].str.replace(",","").astype(int)

    #Convert Crime per 100k population to float
    df['Rate per 100,000 population'] = df['Rate per 100,000 population'].str.replace(",","").astype(float)

    years = df['Year'].unique()

    df_yearlyCrime_HousePrice=[]
    for _, row in df.iterrows():
        year = row['Year']
        if year == max(years):#If it's max years no information supporting the next 9 months of that year so continue
            continue     
        #Get next year row for that council area
        next_year_row = df[(df['Year'] == (row['Year']+ 1)) & (df['Local Government Area'] == row['Local Government Area'])]
        
        #Calculate the monthly stats for next year
        next_year_incidents = round(next_year_row['Incidents Recorded'].sum() / 12, 1)
        next_year_rate = round(next_year_row['Rate per 100,000 population'].sum() / 12, 1)

        #Calculate the monthly stats for this year
        incidents_per_month = round(row['Incidents Recorded'] / 12, 1)
        rate_per_month = round(row['Rate per 100,000 population'] / 12, 1)

        #Times this year by 3 and next year by 9 to get an estimate of what the full January to December Crime rate would be
        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        yearly_rate_per_100k = int(round((rate_per_month * 3) + (next_year_rate * 9), 0))
        
        #Append Data to new Dataframe
        df_yearlyCrime_HousePrice.append({
            "Year": year,
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year,
            "Yearly Rate per 100,000 population": yearly_rate_per_100k
        })
    
    #Convert to Dataframe
    df_yearlyCrime_HousePrice = pd.DataFrame(df_yearlyCrime_HousePrice)

    for _, year in enumerate(df_yearlyCrime_HousePrice["Year"].unique()):
        if year < 2019:
            continue
        futureCrime.update({year: {}})
        for _, councilArea in enumerate(df_yearlyCrime_HousePrice["CouncilArea"].unique()):
            row = df_yearlyCrime_HousePrice[(df_yearlyCrime_HousePrice['Year'] == year) & (df_yearlyCrime_HousePrice['CouncilArea'] == councilArea)]
            futureCrime[year].update({councilArea: {"Yearly Incidents Recorded": row["Yearly Incidents Recorded"].item() , "Yearly Rate per 100,000 population": row["Yearly Rate per 100,000 population"].item()}})

    #Drop any rows with years after 2018
    df_yearlyCrime_HousePrice.drop(df_yearlyCrime_HousePrice[df_yearlyCrime_HousePrice['Year'].astype(int) > 2018].index, inplace = True)

    return df_yearlyCrime_HousePrice

def clean_house_price_data():
    house_price_df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")

    # Dropping rows that has null cells in Price
    house_price_df.dropna(subset=["Price"], inplace=True)

    # Set Year
    house_price_df.rename(columns={'Date': "Year"}, inplace=True)
    house_price_df["Year"] = pd.to_datetime(house_price_df["Year"], format="%d/%m/%Y").dt.year

    #house_price_df["Price"] = house_price_df["Price"].astype(int) / 1_000_000
    
    #Moreland City Council is now Merri-Bek
    house_price_df.loc[(house_price_df['CouncilArea'] == "Moreland City Council"), "CouncilArea"] = "Merri-bek City Council"

    house_price_df.drop(house_price_df[~house_price_df['CouncilArea'].isin(GreaterMelbourneLGAs)].index, inplace = True)

    #Transform "h, u and t" to have a relevant meaning
    #house_price_df['Type'] = house_price_df['Type'].replace({'h': 'House', 'u': 'Unit', 't': 'Townhouse'})
    
    # Drop unecessary columns
    house_price_df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Type", "Postcode", "Regionname", "Propertycount", "Distance"], axis=1, inplace=True)
    
    # Calculate average Price per Year and CouncilArea
    house_price_df = house_price_df.groupby(['Year', 'CouncilArea'])['Price'].mean().reset_index()

    return house_price_df

def add_house_price_data(df):
    # Merge DataFrames on 'CouncilArea' and 'HousingYear' with 'Year' from crime data
    merged_df = pd.merge(clean_house_price_data(), df, left_on=['CouncilArea', 'Year'], right_on=['CouncilArea', 'Year'], how='left')
    
    merged_df.sort_values(by=["Year", "CouncilArea"], ascending=[False,True])

    return merged_df

#Use Polynomial Regression to predict future house prices
def use_polynomial_regression_to_predict_house_price(df):
    
    predicted_prices = []

    # Define predicted years
    predicted_years = [2019, 2020, 2021, 2022, 2023]

    # Define council areas
    council_areas = df['CouncilArea'].unique()
    
    for councilArea in council_areas:
        # Filter data for current council area
        area_df = df[df['CouncilArea'] == councilArea]

        # Define features (X) and target (y)
        X = area_df[['Year', 'Yearly Incidents Recorded', 'Yearly Rate per 100,000 population']]
        Y = area_df['Price']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Define polynomial regression pipeline
        degree = 3  # adjust the degree as needed
        poly_regression = Pipeline([
            ('poly_features', PolynomialFeatures(degree=degree)),
            ('linear_regression', LinearRegression())
        ])

        # Fit the model on the training data
        poly_regression.fit(X_train.values, y_train.values)

        # Predict on the testing data
        y_pred = poly_regression.predict(X_test.values)

        # Calculate mean squared error
        mse = mean_squared_error(y_test.values, y_pred)
        print(f'Council Area: {councilArea}, Mean Squared Error: {mse:.4f}')
    
        # Predict prices for future years
        future_data = np.array([
            [year, futureCrime[year][councilArea]["Yearly Incidents Recorded"] , futureCrime[year][councilArea]["Yearly Rate per 100,000 population"]] 
            for year in predicted_years
        ])
        predictions = poly_regression.predict(future_data)
        for year, price in zip(predicted_years, predictions):
            predicted_prices.append({"Price": price, "Year": year, "CouncilArea": councilArea})
        if True:
            print(f'Predicted Prices for {councilArea}:')
            for year, price in zip(predicted_years, predictions):
                print(f'Year: {year}, Predicted Price: {price:.4f}')

    return pd.DataFrame(predicted_prices)

#Combines the 2016-2018 data with the predicted values
def combine_predictions_with_actual(actual, predicted):
    #Remove unneeded columns
    actual.drop(columns=["Yearly Incidents Recorded", "Yearly Rate per 100,000 population"], axis=1, inplace=True)
    
    #Join DataFrames
    all_data = pd.concat([actual, predicted], ignore_index=True)
    
    #Sort Data
    all_data = all_data.sort_values(by=["Year", "CouncilArea"], ascending=[False,True])

    #price to two decimal places
    all_data['Price'] = all_data['Price'].astype(int)

    return all_data

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
    HousingCrimeDF = add_house_price_data(clean_and_manipulate_crime_data())
    HousingCrimeDF.to_csv("out_crime.csv", index=False)
    predictedFuturePrices = use_polynomial_regression_to_predict_house_price(HousingCrimeDF)
    combinedHousingPriceData = combine_predictions_with_actual(HousingCrimeDF, predictedFuturePrices)
    combinedHousingPriceData.to_csv("out_predictions.csv", index=False)
    plot_future_prices(combinedHousingPriceData)

if __name__ == "__main__":
    main()