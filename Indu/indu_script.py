import pandas as pd
import matplotlib.pyplot as plt

house_prices = pd.read_csv('MELBOURNE_housing_FULL.csv')
population_growth = pd.read_csv('population_2017-18.csv')

house_prices['Date'] = pd.to_datetime(house_prices['Date'], format='%d/%m/%Y')

house_prices['Year'] = house_prices['Date'].dt.year

population_cleaned = population_growth.dropna(axis=1, how='all')

pop_long = population_cleaned.melt(id_vars=['LGA code', ' Local Government Area', ' ERP Change no.', ' ERP change %', ' Natural Increase', ' Net internal migration', ' Net overseas migration',' Area', ' Population Density'], var_name='Year', value_name='Population')

pop_long['Year'] = pd.to_numeric(pop_long['Year'])

pop_long[' Local Government Area'] = pop_long[' Local Government Area'].str.replace(r'\s*\(.*\)', '', regex=True)

house_prices['CouncilArea'] = house_prices['CouncilArea'].str.replace('City Council', '', regex=False).str.strip()

merged_data = pd.merge(house_prices, pop_long, left_on=['CouncilArea', 'Year'], right_on=[' Local Government Area', 'Year'])

merged_data.to_csv('population.csv')