# XGBoost Classification Model to predict house types, made by Indu Seth

import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
import colorama
import clean_data


#Run XGBoost
def main():
    colorama.init()
    print(f"{colorama.Fore.GREEN}XGBoost Classification to predict house types{colorama.Fore.RESET}")
    xgboost()


#Create XGBoost and print out to terminal
def xgboost():
    X, y_encoded, le = clean_data.prep_classify_data()

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=742)

    X_train = X_train.dropna().reset_index(drop=True)
    y_train = y_train[X_train.index]

    smote = SMOTE(random_state=742)

    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    print(f"{colorama.Fore.GREEN}Original training set size:{colorama.Fore.RESET}", X_train.shape, ":", np.bincount(y_train))
    print(f"{colorama.Fore.GREEN}Resampled training set size:{colorama.Fore.RESET}", X_resampled.shape, ":", np.bincount(y_resampled))

    # Train the model with resampled data
    model = xgb.XGBClassifier(objective="multi:softmax", num_class=len(np.unique(y_resampled)))
    model.fit(X_resampled, y_resampled)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Print performance metrics
    print(f"{colorama.Fore.GREEN}Performance metrics for Random Forest Classification{colorama.Fore.RESET}")
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Classification report
    print("Classification Report: \n", classification_report(y_test, y_pred, target_names=le.classes_))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
