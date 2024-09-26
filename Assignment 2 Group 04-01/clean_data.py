import pandas as pd

def clean_housing_data():
    housing_df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")

    #Drop City Council/Shire Council
    housing_df['CouncilArea'] = housing_df['CouncilArea'].str.replace(r' City Council| Shire Council', '', regex=True)

    # Moreland City Council is now Merri-Bek
    housing_df.loc[(housing_df['CouncilArea'] == "Moreland"), "CouncilArea"] = "Merri-bek"

    # Set Year
    housing_df.rename(columns={'Date': "Year"}, inplace=True)
    housing_df["Year"] = pd.to_datetime(housing_df["Year"], format="%d/%m/%Y").dt.year

    return housing_df

def clean_crime_data(local_gov_areas):
    crime_df = pd.read_csv("./datasets/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

    #Remove Police Region, Not applicable for model
    crime_df.drop(columns="Police Region", axis=1, inplace=True)

    #Remove whitespaces on LGA's
    crime_df['Local Government Area'] = crime_df['Local Government Area'].str.strip()

    #Drop any LGA's not in Greater Melbourne
    crime_df.drop(crime_df[~crime_df['Local Government Area'].isin(local_gov_areas)].index, inplace = True)

    #Convert Crimes in LGA to int
    crime_df['Incidents Recorded'] = crime_df['Incidents Recorded'].str.replace(",","").astype(int)

    yearly_crime_df=[]
    for _, row in crime_df.iterrows():
        year = row['Year']
        if year > 2017:#No need to keep years after 2017
            continue     
        #Get next year row for that council area
        next_year_row = crime_df[(crime_df['Year'] == (row['Year']+ 1)) & (crime_df['Local Government Area'] == row['Local Government Area'])]
        
        #Calculate the monthly stats for next year
        next_year_incidents = round(next_year_row['Incidents Recorded'].sum() / 12, 1)

        #Calculate the monthly stats for this year
        incidents_per_month = round(row['Incidents Recorded'] / 12, 1)

        #Times this year by 3 and next year by 9 to get an estimate of what the full January to December Crime rate would be
        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        
        #Append Data to new Dataframe
        yearly_crime_df.append({
            "Year": year + 1, #Add one to merge the 2015 crime with 2016 house data
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year
        })
    pd.DataFrame(yearly_crime_df).to_csv("crime.csv")
    return pd.DataFrame(yearly_crime_df)

def clean_population_data():
    popu_df = pd.read_csv("./datasets/only_population.csv")

    # Remove leading spaces in column names
    popu_df.columns = popu_df.columns.str.strip()

    # Drop N/A columns
    popu_df.dropna(axis=1, how="any", inplace=True)

    popu_df.drop(columns=["LGA code", 'ERP Change no.', 'ERP change %', 'Natural Increase', 'Net internal migration', 'Net overseas migration','Area', "2016", "2017", "2018"], inplace=True)

    # Clean the 'Local Government Area' column by removing text within parentheses and spaces
    popu_df["Local Government Area"] = popu_df["Local Government Area"].str.replace(r'\s*\(.*\)', "", regex=True).str.strip()

    print(popu_df.head())

    return popu_df


def prep_final_data():
    housing_df = clean_housing_data()
    housing_df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Postcode", "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", "Regionname", "Landsize", "Bedroom2"], inplace=True)

    housing_df = housing_df.dropna(axis=0).reset_index(drop=True)

    crime_df = clean_crime_data(housing_df['CouncilArea'].dropna().unique())

    # Merge DataFrames on 'CouncilArea' and 'HousingYear' with 'Year' from crime data
    inter_df = pd.merge(housing_df, crime_df, left_on=['CouncilArea', 'Year'], right_on=['CouncilArea', 'Year'], how='left')

    popu_df = clean_population_data()

    popu_df.rename(columns={'Local Government Area': 'CouncilArea'}, inplace=True)

    merged_df = pd.merge(popu_df, inter_df, how='inner', left_on=['CouncilArea'], right_on=['CouncilArea'])

    merged_df.to_csv("final.csv")

    print(merged_df[['Population Density', 'Price']].corr())

    #Encode the features to be 1 or 0
    df_encoded = pd.get_dummies(merged_df[['CouncilArea', "Type", 'Car', 'Rooms']])
    X = pd.concat([merged_df[['Distance', 'Yearly Incidents Recorded', 'Propertycount', "Population Density"]], df_encoded], axis=1)
    Y = merged_df['Price']

    return X, Y 