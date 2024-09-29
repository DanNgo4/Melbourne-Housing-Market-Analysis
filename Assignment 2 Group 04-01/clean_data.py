import pandas as pd
from sklearn.preprocessing import LabelEncoder
import colorama


colorama.init()

#Returns cleaned housing data
def clean_housing_data():
    housing_df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")

    # Displaying original data
    print(f"{colorama.Fore.GREEN}Original Housing dataset:\n{colorama.Fore.RESET}", str(housing_df))

    #Drop City Council/Shire Council
    housing_df["CouncilArea"] = housing_df["CouncilArea"].str.replace(r" City Council| Shire Council", "", regex=True)

    # Moreland City Council is now Merri-Bek
    housing_df.loc[(housing_df["CouncilArea"] == "Moreland"), "CouncilArea"] = "Merri-bek"

    # Set Year
    housing_df.rename(columns={'Date': "Year"}, inplace=True)
    housing_df["Year"] = pd.to_datetime(housing_df["Year"], format="%d/%m/%Y").dt.year

    # Drop unnecessary columns for all models
    housing_df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Postcode", "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", "Regionname"], inplace=True)

    return housing_df

#Returns the merged datasets for classification models
def prep_classify_data():
    df = clean_housing_data()

    # Drop unecessary columns for the classification models
    df.drop(columns=["Year", "CouncilArea", "Price"], inplace=True)

    # Clean the null entries
    df = df.dropna(axis=0).reset_index(drop=True)

    # Displaying cleaned data
    print(f"{colorama.Fore.GREEN}Dataset after cleaning for Classification models:\n{colorama.Fore.RESET}", str(df))

    # Select features for classification
    features = ["Rooms", "Car", "Propertycount", "Bedroom2", "Landsize", "Distance"]
    X = df[features]  # Independent variables
    y = df["Type"]    # Dependent variable (house type)

    # Encode the target variable (Type)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Cleaned data for Classification models
    df.to_csv("./cleaned_dataset/classification.csv")

    return X, y_encoded, le

#Cleans the crime data
def clean_crime_data(local_gov_areas):
    crime_df = pd.read_csv("./datasets/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

    # Displaying original data
    print(f"{colorama.Fore.GREEN}Original Crime dataset:\n{colorama.Fore.RESET}", str(crime_df))

    # Remove Police Region, Not applicable for model
    crime_df.drop(columns="Police Region", axis=1, inplace=True)

    # Remove whitespaces on LGA's
    crime_df["Local Government Area"] = crime_df["Local Government Area"].str.strip()

    # Drop any LGA's not in Greater Melbourne
    crime_df.drop(crime_df[~crime_df["Local Government Area"].isin(local_gov_areas)].index, inplace = True)

    # Convert Crimes in LGA to int
    crime_df["Incidents Recorded"] = crime_df["Incidents Recorded"].str.replace(",","").astype(int)

    yearly_crime_df=[]
    for _, row in crime_df.iterrows():
        year = row["Year"]
        if year > 2017:# No need to keep years after 2017
            continue     
        # Get next year row for that council area
        next_year_row = crime_df[(crime_df["Year"] == (row["Year"]+ 1)) & (crime_df["Local Government Area"] == row["Local Government Area"])]
        
        # Calculate the monthly stats for next year
        next_year_incidents = round(next_year_row["Incidents Recorded"].sum() / 12, 1)

        # Calculate the monthly stats for this year
        incidents_per_month = round(row["Incidents Recorded"] / 12, 1)

        # Times this year by 3 and next year by 9 to get an estimate of what the full January to December Crime rate would be
        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        
        # Append Data to new Dataframe
        yearly_crime_df.append({
            "Year": year + 1, # Add one to merge the 2015 crime with 2016 house data and so on
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year
        })
    return pd.DataFrame(yearly_crime_df)

#Cleans the population data
def clean_population_data(local_gov_areas):
    popu_df = pd.read_csv("./datasets/population_2017-18.csv")

    # Displaying original data
    print(f"{colorama.Fore.GREEN}Original Population dataset:\n{colorama.Fore.RESET}", str(popu_df))

    # Remove leading spaces in column names
    popu_df.columns = popu_df.columns.str.strip()

    # Drop N/A columns
    popu_df.dropna(axis=1, how="any", inplace=True)

    # Drop un-wanted columns
    popu_df.drop(columns=["LGA code", "ERP Change no.", "ERP change %", "Natural Increase", "Net internal migration", "Net overseas migration", "Area", "2017", "2018"], inplace=True)

    # Clean the Local Government Area column by removing text within parentheses and spaces
    popu_df["Local Government Area"] = popu_df["Local Government Area"].str.replace(r"\s*\(.*\)", "", regex=True).str.strip()

    # Moreland City Council is now Merri-Bek
    popu_df.loc[(popu_df["Local Government Area"] == "Moreland"), "Local Government Area"] = "Merri-bek"

    # Drop any LGA's not in Greater Melbourne
    popu_df.drop(popu_df[~popu_df["Local Government Area"].isin(local_gov_areas)].index, inplace = True)

    return popu_df

#Returns the merged dataframe for regression models
def prep_final_data():
    # Fetching Housing Dataset
    housing_df = clean_housing_data()
    # Drop un-wanted columns for the Regression models
    housing_df.drop(columns=["Bedroom2"], inplace=True)
    # Cleaning the null entries
    housing_df = housing_df.dropna(axis=0).reset_index(drop=True)
    # Define Council Areas that exists in housing_df to filter in crime_df + popu_df
    greater_melbourne = housing_df["CouncilArea"].dropna().unique()

    # Preparing Crime Dataset
    crime_df = clean_crime_data(greater_melbourne)

    # Merge housing_df and crime_df on CouncilArea and Year
    # To create intermediate DataFrame
    inter_df = pd.merge(housing_df, crime_df, left_on=["CouncilArea", "Year"], right_on=["CouncilArea", "Year"], how="left")

    # Drop Year column since it's not needed anymore
    inter_df.drop(columns=["Year"], inplace=True)

    # Preparing Population Dataset
    popu_df = clean_population_data(greater_melbourne)
    popu_df.rename(columns={"Local Government Area": "CouncilArea"}, inplace=True)

    merged_df = pd.merge(popu_df, inter_df, how="inner", left_on=["CouncilArea"], right_on=["CouncilArea"])

    # Displaying cleaned data
    print(f"{colorama.Fore.GREEN}Dataset after cleaning for Regression models:\n{colorama.Fore.RESET}", str(merged_df))

    # Encode the categorical features
    df_encoded = pd.get_dummies(merged_df[["CouncilArea", "Type", "Car", "Rooms"]])
    X = pd.concat([merged_df[["Propertycount", "Distance", "Yearly Incidents Recorded", "Population Density", "Landsize"]], df_encoded], axis=1)
    Y = merged_df["Price"]

    # Cleaned data for Regression models
    merged_df.to_csv("./cleaned_dataset/regression.csv")

    return X, Y