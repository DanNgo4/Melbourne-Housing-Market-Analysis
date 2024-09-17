import pandas as pd

GreaterMelbourneLGAs=["Bayside City Council","Merri-bek City Council","Melbourne City Council","Kingston City Council","Greater Dandenong City Council",
                      "Frankston City Council","Glen Eira City Council","Monash City Council","Stonnington City Council","Port Phillip City Council",
                      "Yarra City Council","Casey City Council","Wyndham City Council","Whittlesea City Council","Nillumbik City Council",
                      "Melton City Council","Moonee Valley City Council","Maribyrnong City Council","Hume City Council","Hobsons Bay City Council",
                      "Darebin City Council","Knox City Council","Brimbank City Council","Banyule City Council","Cardinia City Council","MaroondahCity Council",
                      "Manningham City Council","Boroondara City Council"]

futureCrime={}

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

        #Calculate the monthly stats for this year
        incidents_per_month = round(row['Incidents Recorded'] / 12, 1)

        #Times this year by 3 and next year by 9 to get an estimate of what the full January to December Crime rate would be
        total_crimes_for_year = int(round((incidents_per_month * 3) + (next_year_incidents * 9), 0))
        
        #Append Data to new Dataframe
        df_yearlyCrime_HousePrice.append({
            "Year": year,
            "CouncilArea": row["Local Government Area"],
            "Yearly Incidents Recorded": total_crimes_for_year
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

#Cleans house price data
def clean_house_price_data():
    house_price_df = pd.read_csv("../Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")

    # Dropping rows that has null cells in Price
    house_price_df.dropna(subset=["Price"], inplace=True)

    # Set Year
    house_price_df.rename(columns={'Date': "Year"}, inplace=True)
    house_price_df["Year"] = pd.to_datetime(house_price_df["Year"], format="%d/%m/%Y").dt.year

    #house_price_df["Price"] = house_price_df["Price"].astype(int) / 1_000_000
    
    #Moreland City Council is now Merri-Bek
    house_price_df.loc[(house_price_df['CouncilArea'] == "Moreland City Council"), "CouncilArea"] = "Merri-bek City Council"

    house_price_df.drop(house_price_df[~house_price_df['CouncilArea'].isin(GreaterMelbourneLGAs)].index, inplace = True)
    
    # Calculate average Price per Year and CouncilArea and remove uneccessary columns
    house_price_df = house_price_df.groupby(['Year', 'CouncilArea','Type','Rooms','Distance'])['Price'].mean().reset_index()

    return house_price_df