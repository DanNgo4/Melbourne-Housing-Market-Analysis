import pandas as pd
import matplotlib.pyplot as plt

GreaterMelbourneLGAs=["Bayside","Merri-bek","Melbourne","Kingston","Greater Dandenong","Frankston","Glen Eira","Monash",
                      "Stonnington","Port Phillip","Yarra","Casey","Wyndham","Whittlesea","Nillumbik","Melton","Moonee Valley",
                      "Melbourne","Maribyrnong","Hume","Hobsons Bay","Darebin","Knox","Brimbank","Banyule","Cardinia","Maroondah"
                      ,"Manningham","Boroondara"]

df = pd.read_csv("./Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.csv")

df.drop(columns="Police Region", axis=1, inplace=True)

df['Local Government Area'] = df['Local Government Area'].str.strip()

df.drop(df[~df['Local Government Area'].isin(GreaterMelbourneLGAs)].index, inplace = True)

df.to_csv("out_crime.csv", index=False)