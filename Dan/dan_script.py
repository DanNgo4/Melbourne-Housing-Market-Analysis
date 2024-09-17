import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def main():
    #linear()
    #logistic()
    random_forest()
    #ridge()
    #polynomial()

def linear():
    df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")
    df.dropna(subset=["Price"], inplace=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    x = df[['Rooms', 'Distance']]  # Independent variables
    y = df['Price']  # Dependent variable (house price)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_test['Rooms'], y_test, color="black", label="Actual Values")
    plt.plot(x_test['Rooms'], y_pred, color="blue", linewidth=3, label="Predicted Values")
    plt.xlabel("Rooms")
    plt.ylabel("Price")
    plt.title("Linear Regression on Melbourne Housing Dataset")
    plt.legend()
    plt.show()

def logistic():
    df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")
    df.dropna(subset=["Price"], inplace=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    x = df[['Rooms', 'Distance', 'Price']]  # Independent variables
    y = df['Method']  # Dependent variable (house price)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Classification Report
    report = classification_report(y_test, y_pred, output_dict=True)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", conf_matrix)

    # Visualization: Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False, 
                xticklabels=model.classes_, yticklabels=model.classes_)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.show()

    # Visualization: Precision, Recall, F1-Score
    metrics_df = pd.DataFrame(report).T.drop(['accuracy', 'macro avg', 'weighted avg'], axis=0)
    
    metrics_df[['precision', 'recall', 'f1-score']].plot(kind='bar', figsize=(10, 6))
    plt.title("Precision, Recall, F1-Score per Class")
    plt.ylabel("Score")
    plt.xlabel("Class")
    plt.ylim(0, 1)
    plt.show()

    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plt.scatter(x_test['Rooms'], y_test, color="black", label="Actual Prices (Rooms)")
    plt.scatter(x_test['Rooms'], y_pred, color="blue", label="Predicted Prices (Rooms)")
    plt.xlabel("Number of Rooms")
    plt.ylabel("Price")
    plt.title("Linear Regression: Predicted vs Actual Prices by Rooms")
    plt.legend()
    plt.show()

def random_forest():
    df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")

    df = df.dropna(axis=0).reset_index(drop=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Select features (Rooms, Distance, Propertycount) and target (Price)
    x = df[['Rooms', 'Propertycount', "Distance"]]  # Independent variables
    y = df['Price']  # Dependent variable (house price) 

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Random Forest Regression model
    model = RandomForestRegressor(n_estimators=100)
    model.fit(x_train_scaled, y_train)

    # Predictions
    y_pred = model.predict(x_test_scaled)

    # Evaluate the model
    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    # Plot actual vs predicted prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linewidth=2)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Random Forest Regression on Melbourne Housing Dataset")
    plt.show()

def ridge():
    df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")
    df.dropna(subset=["Price"], inplace=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    x = df[['Rooms', 'Distance', 'Propertycount']]  # Independent variables
    y = df['Price']  # Dependent variable (house price)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Feature scaling
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Hyperparameter tuning for Ridge Regression using GridSearchCV
    ridge_model = Ridge()
    parameters = {'alpha': [0.1, 1.0, 10.0, 100.0]}
    ridge_cv = GridSearchCV(ridge_model, parameters, scoring='r2', cv=5)
    ridge_cv.fit(x_train_scaled, y_train)

    # Best Ridge model
    best_ridge = ridge_cv.best_estimator_

    y_pred = best_ridge.predict(x_test_scaled)

    # Evaluate the model
    print("Best Alpha: ", ridge_cv.best_params_['alpha'])
    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    # Plot predictions vs actual prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue", label="Predicted vs Actual")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--", label="Ideal Fit")
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Ridge Regression: Predicted vs Actual House Prices")
    plt.legend()
    plt.show()

def polynomial():
    df = pd.read_csv("./Dan/MELBOURNE_HOUSE_PRICES_LESS.csv")
    df.dropna(subset=["Price"], inplace=True)

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    X = df[['Rooms', 'Distance']]  # Independent variables
    y = df['Price']  # Dependent variable (house price)

        # Feature scaling before polynomial transformation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create polynomial features (degree=2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X_scaled)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

    # Fit the Polynomial Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicting the test set results
    y_pred = model.predict(X_test)

    # Print performance metrics
    print("Mean Squared Error: %.2f" % mean_squared_error(y_test, y_pred))
    print("R^2 Score: %.2f" % r2_score(y_test, y_pred))

    # Visualization: Predicted vs Actual Prices
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, color="blue", label="Predicted vs Actual")
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linestyle="--", label="Ideal Fit")
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Polynomial Regression (Degree 2): Predicted vs Actual House Prices")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()