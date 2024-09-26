import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import clean_data

def main():
    rf_regression()

def rf_regression():
    x, y = clean_data.prep_final_data()

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=724)

    print("Number of training entries after filtering: ", len(x_train))

    # Random Forest Regression model
    model = RandomForestRegressor(n_estimators=100, random_state=724)
    model.fit(x_train, y_train)

    # Predictions
    y_pred = model.predict(x_test)

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