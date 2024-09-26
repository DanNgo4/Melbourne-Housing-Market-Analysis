# Random Forest Classification Model to predict house types, made by Dan Ngo

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.utils import resample
import clean_data


def main():
    print("Random Forest Classification to predict house types")
    rf_classification()


def rf_classification():
    X, y_encoded, le = clean_data.prep_classify_data()

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
    print("Accuracy: %.2f" % accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


def resample_imbalance(X, y):
    # Resample the dataset to handle class imbalance
    df_resampled = pd.concat([pd.DataFrame(X), pd.DataFrame(y, columns=["Type"])], axis=1)
    df_majority = df_resampled[df_resampled["Type"] == df_resampled["Type"].value_counts().idxmax()]
    df_minority = df_resampled[df_resampled["Type"] != df_resampled["Type"].value_counts().idxmax()]

    df_minority_upsampled = resample(df_minority,
                                     replace=True,  # sample with replacement
                                     n_samples=len(df_majority),  # to match majority class
                                     random_state=123)

    df_upsampled = pd.concat([df_majority, df_minority_upsampled])

    X_resampled = df_upsampled.drop("Type", axis=1).values
    y_resampled = df_upsampled["Type"].values

    return X_resampled, y_resampled


if __name__ == "__main__":
    main()
