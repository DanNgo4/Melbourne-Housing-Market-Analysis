import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

GreaterMelbourneLGAs=["Bayside City Council","Merri-bek City Council","Melbourne City Council","Kingston City Council","Greater Dandenong City Council",
                      "Frankston City Council","Glen Eira City Council","Monash City Council","Stonnington City Council","Port Phillip City Council",
                      "Yarra City Council","Casey City Council","Wyndham City Council","Whittlesea City Council","Nillumbik City Council",
                      "Melton City Council","Moonee Valley City Council","Maribyrnong City Council","Hume City Council","Hobsons Bay City Council",
                      "Darebin City Council","Knox City Council","Brimbank City Council","Banyule City Council","Cardinia City Council","MaroondahCity Council",
                      "Manningham City Council","Boroondara City Council"]

#Merge all data
def merge_all_data():
    # Merge DataFrames on 'CouncilArea' and 'HousingYear' with 'Year' from crime data
    merged_df = pd.merge(clean_house_price_data(), clean_and_manipulate_crime_data(), left_on=['CouncilArea', 'Year'], right_on=['CouncilArea', 'Year'], how='left')
    
    #Sort them in Year than Council 
    merged_df.sort_values(by=["Year", "CouncilArea"], ascending=[False,True])

    return merged_df

#Cleans the Data and manipulates crime data
def clean_and_manipulate_crime_data():

    df = pd.read_csv("./Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

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

    df_yearlyCrime_HousePrice=[]
    for _, row in df.iterrows():
        year = row['Year']
        if year > 2017:#No need to keep years after 2017
            continue     
        #Get next year row for that council area
        next_year_row = df[(df['Year'] == (row['Year']+ 1)) & (df['Local Government Area'] == row['Local Government Area'])]
        
        #Calculate the monthly stats for next year
        next_year_incidents = round(next_year_row['Incidents Recorded'].sum() / 12, 1)

        #Calculate the monthly stats for this year
        incidents_per_month = round(row['Incidents Recorded'] / 12, 1)

        #Times this year by 3 and next year by 9 to get an estimate of what the full January to December Crime rate would be
        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        
        #Append Data to new Dataframe
        df_yearlyCrime_HousePrice.append({
            "Year": year + 1,
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year
        })
    
    return pd.DataFrame(df_yearlyCrime_HousePrice)

#Cleans house price data
def clean_house_price_data():
    house_price_df = pd.read_csv("../Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")

    # Dropping rows that has null cells in Price
    house_price_df.dropna(subset=["Price"], inplace=True)

    # Set Year
    house_price_df.rename(columns={'Date': "Year"}, inplace=True)
    house_price_df["Year"] = pd.to_datetime(house_price_df["Year"], format="%d/%m/%Y").dt.year
    
    #Moreland City Council is now Merri-Bek
    house_price_df.loc[(house_price_df['CouncilArea'] == "Moreland City Council"), "CouncilArea"] = "Merri-bek City Council"

    house_price_df.drop(house_price_df[~house_price_df['CouncilArea'].isin(GreaterMelbourneLGAs)].index, inplace = True)
    
    # Calculate average Price per Year and CouncilArea and remove uneccessary columns
    house_price_df = house_price_df.groupby(['Year', 'CouncilArea','Type','Rooms','Distance'])['Price'].mean().reset_index()

    return house_price_df

def use_polynomial_regression_to_predict_house_price(df):
    #Encode the features to be 1 or 0
    df_encoded = pd.get_dummies(df[['CouncilArea', 'Type']])
    X = pd.concat([df[['Distance', 'Rooms', 'Yearly Incidents Recorded']], df_encoded], axis=1)
    Y = df['Price']

    # Create polynomial features
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_poly, Y, test_size=0.2, random_state=42)


    # Fit the model 
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Print performance metrics
    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))
    return y_test, y_pred

#Plot Predicted Vs Actual based on crime
def plot_predicted_prices(y_test, y_pred):  
    #Line for best fit, Scatter for actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue", label="Predicted vs Actual")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--", label="Ideal Fit")
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Polynomial Regression (Degree 2): Predicted vs Actual House Prices")
    plt.legend()
    plt.show()

#Merges the data than runs poly
def run_poly():
    plot_predicted_prices(use_polynomial_regression_to_predict_house_price(merge_all_data()))

if __name__ == "__main__":
    run_poly()