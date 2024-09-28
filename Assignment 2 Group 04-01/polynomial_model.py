# Polynomial Regression Model to predict housing price, made by Mitchell Henry

import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
import colorama
import clean_data


def main():
    colorama.init()
    print(f"{colorama.Fore.GREEN}Polynomial Regression to predict housing price{colorama.Fore.RESET}")
    run_poly()


def use_polynomial_regression_to_predict_house_price():
    X, Y = clean_data.prep_final_data()

    # Create polynomial features
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_poly, Y, test_size=0.2, random_state=724)

    # Fit the model 
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Print performance metrics
    print(f"{colorama.Fore.GREEN}Performance metrics for Polynomial Regression{colorama.Fore.RESET}")
    print("Mean Absolute Error: %.2f" % mean_absolute_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    return y_test, y_pred


# Plot Predicted Vs Actual based on crime
def plot_predicted_prices(y_test, y_pred):
    # Line for best fit, Scatter for actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue", label="Predicted vs Actual")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--", label="Ideal Fit")
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Polynomial Regression (Degree 2): Predicted vs Actual House Prices")
    plt.legend()
    plt.show()


# Runs everything
def run_poly():
    y_test, y_pred = use_polynomial_regression_to_predict_house_price()
    plot_predicted_prices(y_test, y_pred)


if __name__ == "__main__":
    main()