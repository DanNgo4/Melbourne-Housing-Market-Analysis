import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample
import clean_data


class RFHouseTypeModel:
    def __init__(self):
        self.model = None  
        self.encoder = None 


    def rf_classification(self):
        X, y_encoded, self.encoder = clean_data.prep_classify_data()

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


    def classify(self, square_metres, distance, rooms, cars):
        feature1_default = 0 
        feature2_default = 0 

        input_features = np.array([[square_metres, distance, rooms, cars, feature1_default, feature2_default]])
        predicted_label = self.model.predict(input_features)
        predicted_type = self.encoder.inverse_transform(predicted_label)  

        return predicted_type[0]
    