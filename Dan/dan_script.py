import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler


def main():
    random_forest()


def random_forest():
    df = pd.read_csv("./Dan/Melbourne_housing_FULL.csv")

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    df = df[df["Price"] <= 4000000]

    df.drop(columns=["Suburb", "Address", "Type", "Method", "SellerG", "Date", "Postcode", "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", "Regionname", "CouncilArea"], inplace=True)

    df = df.dropna(axis=0).reset_index(drop=True)

    print("Number of remaining entries: ", len(df))

    # Select features (Rooms, Distance, Propertycount) and target (Price)
    x = df[["Rooms", "Propertycount", "Distance", "Car", "Landsize", "Bedroom2"]]  # Independent variables
    y = df["Price"]  # Dependent variable (house price) 

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Random Forest Regression model
    model = RandomForestRegressor(n_estimators=100, random_state=123)
    model.fit(x_train_scaled, y_train)

    # Predictions
    y_pred = model.predict(x_test_scaled)

    # Evaluate the model
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    # Plot actual vs predicted prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linewidth=2)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Random Forest Regression on Melbourne Housing Dataset")
    plt.show()


if __name__ == "__main__":
    main()