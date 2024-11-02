import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample
import clean_data


class RFHouseTypeModel:
    def __init__(self):
        self.clf = None
        self.le = None
        self.propertycount_mean = None
        self.bedroom2_mean = None
        self.train_model()


    def train_model(self):
        X, y_encoded, self.encoder, propertycount_mean, bedroom2_mean = clean_data.prep_classify_data()
        
        # Set the mean values for defaults
        self.propertycount_mean = propertycount_mean
        self.bedroom2_mean = bedroom2_mean

        X_resampled, y_resampled = self.resample_imbalance(X, y_encoded)

        X_train, _, y_train, _ = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=123)

        self.model = RandomForestClassifier(n_estimators=100, random_state=123)
        self.model.fit(X_train, y_train)


    def resample_imbalance(self, X, y):
        df_resampled = pd.concat([pd.DataFrame(X), pd.DataFrame(y, columns=["Type"])], axis=1)

        df_majority = df_resampled[df_resampled["Type"] == df_resampled["Type"].value_counts().idxmax()]
        df_minority = df_resampled[df_resampled["Type"] != df_resampled["Type"].value_counts().idxmax()]

        df_minority_upsampled = resample(df_minority,
                                         replace=True,  
                                         n_samples=len(df_majority),  
                                         random_state=123)

        df_upsampled = pd.concat([df_majority, df_minority_upsampled])

        X_resampled = df_upsampled.drop("Type", axis=1).values
        y_resampled = df_upsampled["Type"].values

        return X_resampled, y_resampled


    def classify(self, rooms, cars, square_metres, distance):
        # Use mean values as defaults for missing features
        input_features = np.array([[rooms, cars, self.propertycount_mean, self.bedroom2_mean, square_metres, distance]])
        predicted_label = self.model.predict(input_features)
        predicted_type = self.encoder.inverse_transform(predicted_label)  

        return predicted_type[0]
    