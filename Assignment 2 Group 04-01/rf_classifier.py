import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils import resample
import clean_data


def main():
    rf_classification()


def rf_classification():
    df = clean_data.clean_housing_data()

    df.drop(columns=["Suburb", "Address", "Method", "SellerG", "Year", "Postcode", 
                     "Bathroom", "BuildingArea", "YearBuilt", "Longtitude", "Lattitude", 
                     "Regionname", "CouncilArea", "Price"], inplace=True)

    # Data preprocessing
    df = df.dropna(axis=0).reset_index(drop=True)

    # Select features for classification
    features = ['Rooms', 'Car', 'Propertycount', 'Bedroom2', 'Landsize']
    X = df[features]  # Independent variables
    y = df['Type']    # Dependent variable (house type)

    # Encode the target variable (Type)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Handle class imbalance
    X_resampled, y_resampled = resample_imbalance(X_scaled, y_encoded)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=123)


    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=123)
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred, target_names=le.classes_)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print("Accuracy: %.2f" % accuracy)
    print(classification_rep)
    print("Confusion Matrix:\n", conf_matrix)


def resample_imbalance(X, y):
    # Resample the dataset to handle class imbalance
    df_resampled = pd.concat([pd.DataFrame(X), pd.DataFrame(y, columns=['Type'])], axis=1)
    df_majority = df_resampled[df_resampled['Type'] == df_resampled['Type'].value_counts().idxmax()]
    df_minority = df_resampled[df_resampled['Type'] != df_resampled['Type'].value_counts().idxmax()]

    df_minority_upsampled = resample(df_minority,
                                     replace=True,  # sample with replacement
                                     n_samples=len(df_majority),  # to match majority class
                                     random_state=123)

    df_upsampled = pd.concat([df_majority, df_minority_upsampled])

    X_resampled = df_upsampled.drop('Type', axis=1).values
    y_resampled = df_upsampled['Type'].values

    return X_resampled, y_resampled


if __name__ == "__main__":
    main()
