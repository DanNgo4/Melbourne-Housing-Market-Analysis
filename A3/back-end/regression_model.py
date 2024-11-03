from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import clean_data
import pandas as pd
from sklearn.impute import SimpleImputer
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
import colorama


class RFHousePriceModel:
    def __init__(self):
        colorama.init()
        self.model = RandomForestRegressor(n_estimators=100, random_state=724)
        self.default_values = None
        self._train_model()

    def _train_model(self):
        x, y = clean_data.prep_final_data()
        
        self.imputer = SimpleImputer(missing_values=pd.NA, strategy="mean")
        x_imputed = pd.DataFrame(self.imputer.fit_transform(x), columns=x.columns)

        self.default_values = x_imputed.mean()

        x_train, x_test, y_train, y_test = train_test_split(x_imputed, y, test_size=0.2, random_state=724)
        self.model.fit(x_train, y_train)

        joblib.dump(self.model, "rf_house_price_model.pkl")

        y_pred = self.model.predict(x_test)

        print(f"{colorama.Fore.GREEN}Performance metrics for Random Forest Regression{colorama.Fore.RESET}")
        print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, y_pred))
        print("R^2 Score: %.2f" % r2_score(y_test, y_pred))


    def predict(self, square_metres, distance, rooms, cars):
        model = joblib.load("rf_house_price_model.pkl")

        input_data = self.default_values.copy()

        input_data["Landsize"] = square_metres
        input_data["Distance"] = distance
        input_data["Room"] = rooms
        input_data["Car"] = cars
        
        input_data_df = pd.DataFrame([input_data], columns=self.default_values.index)

        return model.predict(input_data_df)
