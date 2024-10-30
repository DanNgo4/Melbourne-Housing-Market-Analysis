import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import clean_data

class RFHousePriceModel:
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=123)
        self.scaler = StandardScaler()

    def train_rf(self):
        x, y = clean_data.clean_housing_data()
        # Split data into training and testing sets
        x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=123)

        self.model.fit(x_train, y_train)

         # Save the model
        joblib.dump(self.model, 'simple_model.pkl')

def predict(square_metres, car, distance, property_count):
        # Load the model
        model = joblib.load('rf_house_price_model.pkl')
        
        # Make a prediction based on input
        return model.predict([[square_metres, car, distance, property_count]])

if __name__ == "__main__":
    model = RFHousePriceModel()
    model.train_rf()