import pandas as pd

def clean_housing_data():
    housing_df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")


    print("CouncilAreas null: ", housing_df['CouncilArea'].isnull().sum())
    housing_df.dropna(subset=["CouncilArea"], inplace=True)

    #Drop City Council/Shire Council
    housing_df['CouncilArea'] = housing_df['CouncilArea'].str.replace(r' City Council| Shire Council', '', regex=True)

    # Moreland City Council is now Merri-Bek
    housing_df.loc[(housing_df['CouncilArea'] == "Moreland"), "CouncilArea"] = "Merri-bek"


    housing_df = housing_df.dropna(axis=0).reset_index(drop=True)

    # Align date format
    housing_df["Date"] = pd.to_datetime(housing_df["Date"], format="%d/%m/%Y")
    # Set Year
    housing_df.rename(columns={'Date': "Year"}, inplace=True)
    housing_df["Year"] = pd.to_datetime(housing_df["Year"], format="%d/%m/%Y").dt.year

    housing_df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Postcode", 
                     "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", 
                     "Regionname"], inplace=True)
    housing_df.to_csv("house.csv")
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

def prep_crime_housing_data():
    housing_df = clean_housing_data()

    # Merge DataFrames on 'CouncilArea' and 'HousingYear' with 'Year' from crime data
    merged_df = pd.merge(housing_df, clean_crime_data(housing_df['CouncilArea'].dropna().unique()), left_on=['CouncilArea', 'Year'], right_on=['CouncilArea', 'Year'], how='left')
    
    #Sort them in Year than Council 
    merged_df.sort_values(by=["Year", "CouncilArea"], ascending=[False,True])

    print("Final length: ", len(merged_df))

    #Encode the features to be 1 or 0
    df_encoded = pd.get_dummies(merged_df[['CouncilArea', 'Type']])
    X = pd.concat([merged_df[['Distance', 'Car', 'Rooms', 'Propertycount', 'Yearly Incidents Recorded']], df_encoded], axis=1)
    Y = merged_df['Price']

    X.to_csv('out.csv')

    return X, Y 