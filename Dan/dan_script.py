import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder


def main():
    # random_forest()
    rf()


def random_forest():
    df = pd.read_csv("./Dan/Melbourne_housing_FULL.csv")

    # Align date format
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

    df = df[df["Price"] <= 4000000]

    df.drop(columns=["Suburb", "Address", "Type", "Method", "SellerG", "Date", "Postcode", 
                     "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", 
                     "Regionname", "CouncilArea"], inplace=True)

    # Drop rows with missing values
    df = df.dropna(axis=0).reset_index(drop=True)

    print("Number of remaining entries: ", len(df))

    # Select features (Rooms, Distance, Propertycount, etc.) and target (Price)
    x = df[["Rooms", "Propertycount", "Distance", "Car", "Landsize", "Bedroom2"]]  # Independent variables
    y = df["Price"]  # Dependent variable (house price)

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)

    # Drop house prices > 4 million from the training set only
    train_mask = y_train <= 4000000
    x_train = x_train[train_mask]
    y_train = y_train[train_mask]

    print("Number of training entries after filtering: ", len(x_train))

    # Standardize features
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


def rf():
    df = pd.read_csv("./Dan/Melbourne_housing_FULL.csv")

    df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Date", "Postcode", 
                     "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", 
                     "Regionname", "CouncilArea"], inplace=True)

    # Data preprocessing
    df = df.dropna(subset=['Type'])  # Drop rows where 'Type' is missing

    # Select features for classification
    features = ['Rooms', "Price", 'Car', 'Landsize', 'Propertycount', 'Bedroom2']
    X = df[features]  # Independent variables
    y = df['Type']    # Dependent variable (house type)

    # Drop rows with missing values in the features
    X = X.dropna()
    y = y[X.index]  # Ensure y matches the indices after dropping

    # Encode the target variable (Type)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=123)

    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=123)
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred, target_names=le.classes_)

    print("Accuracy: %.2f" % accuracy)
    print(classification_rep)


if __name__ == "__main__":
    main()