import pandas as pd
from sklearn.preprocessing import LabelEncoder
import colorama


colorama.init()


#Returns cleaned housing data
def clean_housing_data():
    housing_df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")

    #Drop all null columns
    housing_df = housing_df.dropna(axis=0).reset_index(drop=True)

    # Drop unnecessary columns for all models
    housing_df.drop(columns=["Rooms","Bedroom2","Type","Suburb", "Address", "Method", "SellerG", "CouncilArea", "Date", "Postcode", "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", "Regionname"], inplace=True)

    housing_df = housing_df[housing_df["Landsize"] > 0]

    #Leaving Price, Distance, Car, Landsize, Propertycount
    housing_df[["Landsize", "Car", "Distance", "Propertycount"]].to_csv("predicted_values.csv",index=False)

    return housing_df[["Landsize", "Car", "Distance", "Propertycount"]], housing_df["Price"]

if __name__ == "__main__":
    clean_housing_data()