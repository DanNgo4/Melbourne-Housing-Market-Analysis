from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import clean_data
import colorama
import pandas as pd
from sklearn.impute import SimpleImputer


class RFHousePriceModel:
    def __init__(self):
        self.model = None
        self.default_values = None
        self.imputer = None
        self._train_model()

    def _train_model(self):
        x, y = clean_data.prep_final_data()
        
        # Impute missing values using mean for features
        self.imputer = SimpleImputer(missing_values=pd.NA, strategy='mean')
        x_imputed = pd.DataFrame(self.imputer.fit_transform(x), columns=x.columns)

        # Store mean values for features to use as defaults
        self.default_values = x_imputed.mean()

        x_train, x_test, y_train, y_test = train_test_split(x_imputed, y, test_size=0.2, random_state=724)
        self.model = RandomForestRegressor(n_estimators=100, random_state=724)
        self.model.fit(x_train, y_train)

        # Performance metrics
        y_pred = self.model.predict(x_test)
        print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
        print(f"R^2 Score: {r2_score(y_test, y_pred):.2f}")

    def predict(self, square_metres, distance, propertycount):
        # Ensure input_data is a copy of the default values with all features
        input_data = self.default_values.copy()

        # Update with user-provided inputs
        input_data["Landsize"] = square_metres
        input_data["Distance"] = distance
        input_data["Propertycount"] = propertycount
        
        # Convert input_data to a DataFrame with the correct columns
        input_data_df = pd.DataFrame([input_data], columns=self.default_values.index)
        
        # Debugging: Check the structure of the DataFrame
        print("Input DataFrame for prediction:")
        print(input_data_df)

        # Impute any missing values in the input data
        input_data_imputed = pd.DataFrame(self.imputer.transform(input_data_df), columns=input_data_df.columns)

        # Predict with the imputed input data
        return self.model.predict(input_data_df)
