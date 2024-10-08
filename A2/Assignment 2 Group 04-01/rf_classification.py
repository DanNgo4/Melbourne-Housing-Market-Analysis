# Random Forest Classification Model to predict house types, made by Dan Ngo

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils import resample
import colorama
import clean_data


#Run RF classification
def main():
    colorama.init()
    print(f"{colorama.Fore.GREEN}Random Forest Classification to predict house types{colorama.Fore.RESET}")
    rf_classification()


#Create RF clasification and print results to terminal
def rf_classification():
    X, y_encoded, le = clean_data.prep_classify_data()

    # Handle class imbalance    
    X_resampled, y_resampled = resample_imbalance(X, y_encoded)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=123)

    print(f"{colorama.Fore.GREEN}Original training set size:{colorama.Fore.RESET}", X_train.shape, ":", np.bincount(y_train))
    print(f"{colorama.Fore.GREEN}Resampled training set size:{colorama.Fore.RESET}", X_resampled.shape, ":", np.bincount(y_resampled))

    # Train the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=123)
    clf.fit(X_train, y_train)

    # Make predictions
    y_pred = clf.predict(X_test)

    # Print performance metrics
    print(f"{colorama.Fore.GREEN}Performance metrics for Random Forest Classification{colorama.Fore.RESET}")
    print("Accuracy: %.2f" % accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


# Resample the dataset to handle class imbalance
def resample_imbalance(X, y):
    # re-combine the features back to a dataframe
    df_resampled = pd.concat([pd.DataFrame(X), pd.DataFrame(y, columns=["Type"])], axis=1)

    # identify majority and minority classes
    df_majority = df_resampled[df_resampled["Type"] == df_resampled["Type"].value_counts().idxmax()]
    df_minority = df_resampled[df_resampled["Type"] != df_resampled["Type"].value_counts().idxmax()]

    # Up-sampling the minority class
    df_minority_upsampled = resample(df_minority,
                                     replace=True,  # sample with replacement
                                     n_samples=len(df_majority),  # to match majority class
                                     random_state=123)

    # re-combining the re-sampled data
    df_upsampled = pd.concat([df_majority, df_minority_upsampled])

    # re-separating the features and labels
    X_resampled = df_upsampled.drop("Type", axis=1).values
    y_resampled = df_upsampled["Type"].values

    return X_resampled, y_resampled


if __name__ == "__main__":
    main()
