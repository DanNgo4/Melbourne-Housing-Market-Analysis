import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_housing_data():
    housing_df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")

    housing_df["CouncilArea"] = housing_df["CouncilArea"].str.replace(r" City Council| Shire Council", "", regex=True)

    housing_df.loc[(housing_df["CouncilArea"] == "Moreland"), "CouncilArea"] = "Merri-bek"

    housing_df.rename(columns={"Date": "Year"}, inplace=True)
    housing_df["Year"] = pd.to_datetime(housing_df["Year"], format="%d/%m/%Y").dt.year

    housing_df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Postcode", "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", "Regionname"], inplace=True)

    return housing_df


def prep_classify_data():
    df = clean_housing_data()

    df.drop(columns=["Year", "CouncilArea", "Price"], inplace=True)
    df = df.dropna(axis=0).reset_index(drop=True)

    features = ["Rooms", "Car", "Propertycount", "Bedroom2", "Landsize", "Distance"]
    X = df[features]
    y = df["Type"]

    propertycount_mean = X["Propertycount"].mean()
    bedroom2_mean = X["Bedroom2"].mean()

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le, propertycount_mean, bedroom2_mean


def clean_crime_data(local_gov_areas):
    crime_df = pd.read_csv("./datasets/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

    crime_df.drop(columns="Police Region", axis=1, inplace=True)

    crime_df["Local Government Area"] = crime_df["Local Government Area"].str.strip()

    crime_df.drop(crime_df[~crime_df["Local Government Area"].isin(local_gov_areas)].index, inplace = True)

    crime_df["Incidents Recorded"] = crime_df["Incidents Recorded"].str.replace(",","").astype(int)

    yearly_crime_df=[]
    for _, row in crime_df.iterrows():
        year = row["Year"]
        if year > 2017:
            continue     
        next_year_row = crime_df[(crime_df["Year"] == (row["Year"]+ 1)) & (crime_df["Local Government Area"] == row["Local Government Area"])]
        
        next_year_incidents = round(next_year_row["Incidents Recorded"].sum() / 12, 1)

        incidents_per_month = round(row["Incidents Recorded"] / 12, 1)

        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        
        yearly_crime_df.append({
            "Year": year + 1,
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year
        })
        
    return pd.DataFrame(yearly_crime_df)


def clean_population_data(local_gov_areas):
    popu_df = pd.read_csv("./datasets/population_2017-18.csv")

    popu_df.columns = popu_df.columns.str.strip()

    popu_df.dropna(axis=1, how="any", inplace=True)

    popu_df.drop(columns=["LGA code", "ERP Change no.", "ERP change %", "Natural Increase", "Net internal migration", "Net overseas migration", "Area", "2017", "2018"], inplace=True)

    popu_df["Local Government Area"] = popu_df["Local Government Area"].str.replace(r"\s*\(.*\)", "", regex=True).str.strip()

    popu_df.loc[(popu_df["Local Government Area"] == "Moreland"), "Local Government Area"] = "Merri-bek"

    popu_df.drop(popu_df[~popu_df["Local Government Area"].isin(local_gov_areas)].index, inplace = True)

    return popu_df


def prep_final_data():
    housing_df = clean_housing_data()
    housing_df.drop(columns=["Bedroom2"], inplace=True)
    housing_df = housing_df.dropna(axis=0).reset_index(drop=True)
    greater_melbourne = housing_df["CouncilArea"].dropna().unique()

    crime_df = clean_crime_data(greater_melbourne)

    inter_df = pd.merge(housing_df, crime_df, left_on=["CouncilArea", "Year"], right_on=["CouncilArea", "Year"], how="left")

    inter_df.drop(columns=["Year"], inplace=True)

    popu_df = clean_population_data(greater_melbourne)
    popu_df.rename(columns={"Local Government Area": "CouncilArea"}, inplace=True)

    merged_df = pd.merge(popu_df, inter_df, how="inner", left_on=["CouncilArea"], right_on=["CouncilArea"])

    df_encoded = pd.get_dummies(merged_df[["CouncilArea", "Type"]])
    X = pd.concat([merged_df[["Propertycount", "Distance", "Yearly Incidents Recorded", "Population Density", "Landsize", "Rooms", "Car"]], df_encoded], axis=1)
    Y = merged_df["Price"]

    return X, Y
