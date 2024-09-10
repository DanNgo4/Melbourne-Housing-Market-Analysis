import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

GreaterMelbourneLGAs=["Bayside","Merri-bek","Melbourne","Kingston","Greater Dandenong","Frankston","Glen Eira","Monash",
                      "Stonnington","Port Phillip","Yarra","Casey","Wyndham","Whittlesea","Nillumbik","Melton","Moonee Valley",
                      "Melbourne","Maribyrnong","Hume","Hobsons Bay","Darebin","Knox","Brimbank","Banyule","Cardinia","Maroondah"
                      ,"Manningham","Boroondara"]

df = pd.read_csv("./Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

#Remove Police Region, Not applicable for model
df.drop(columns="Police Region", axis=1, inplace=True)

#Remove whitespaces on LGA's
df['Local Government Area'] = df['Local Government Area'].str.strip()

#Drop any LGA's not in Greater Melbourne
df.drop(df[~df['Local Government Area'].isin(GreaterMelbourneLGAs)].index, inplace = True)

#Append " City Council" to end to match LGA column in Housing price dataset
df['Local Government Area'] = df['Local Government Area'] + " City Council"

#Convert Crimes in LGA to int
df['Incidents Recorded'] = df['Incidents Recorded'].str.replace(",","").astype(int)

#Convert Crime per 100k population to float
df['Rate per 100,000 population'] = df['Rate per 100,000 population'].str.replace(",","").astype(float)

years = df['Year'].unique()

df_yearlyAvg=[]
for index, row in df.iterrows():
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
    df_yearlyAvg.append({
        "Year": year,
        "CouncilArea": row["Local Government Area"],
        "Yearly Incidents Recorded": total_crimes_for_year,
        "Yearly Rate per 100,000 population": yearly_rate_per_100k
    })

#Convert to Dataframe
df_yearlyAvg = pd.DataFrame(df_yearlyAvg)

#Sort by Date than CouncilArea
df_yearlyAvg = df_yearlyAvg.sort_values(by=["Year", "CouncilArea"], ascending=[False,True])

#Output to CSV
df_yearlyAvg.to_csv("out_crime.csv", index=False)

#Initialise Matplotlib
plt.figure(figsize=(25, 15))
plt.style.use('seaborn-v0_8-darkgrid')

# Get all the councils
councils = df_yearlyAvg["CouncilArea"].unique()
# Colors for each council
colors = plt.cm.get_cmap('hsv', len(councils))

#plot each council
for index, council in enumerate(councils):
    council_data = df_yearlyAvg[df_yearlyAvg["CouncilArea"] == council]
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