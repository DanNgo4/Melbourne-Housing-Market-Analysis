# Random Forest Regression Model to predict housing price, made by Dan Ngo

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import colorama
import clean_data


def main():
    colorama.init()
    print(f"{colorama.Fore.GREEN}Random Forest Regresssion to predict housing price{colorama.Fore.RESET}")
    rf_regression()


def rf_regression():
    x, y = clean_data.prep_final_data()

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=724)

    # Random Forest Regression model
    model = RandomForestRegressor(n_estimators=100, random_state=724)
    model.fit(x_train, y_train)

    # Predictions
    y_pred = model.predict(x_test)

    # Print performance metrics
    print(f"{colorama.Fore.GREEN}Performance metrics for Random Forest Regression{colorama.Fore.RESET}")
    print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, y_pred))
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