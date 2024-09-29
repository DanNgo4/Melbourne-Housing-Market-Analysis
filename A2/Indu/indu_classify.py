import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

df = pd.read_csv('MELBOURNE_HOUSE_PRICES_LESS.csv')

le = LabelEncoder()

df['Type_encoded'] = le.fit_transform(df['Type'])

# Features (X)
X = df[['Rooms', 'Price', 'Distance', 'Propertycount']]

# Target (y) - the encoded house type
y = df['Type_encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = X_train.dropna()
y_train = y_train[X_train.index]

smote = SMOTE(random_state=42)

X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

print("Original training set size:", X_train.shape, ":", np.bincount(y_train))
print("Resampled training set size:", X_resampled.shape, ":", np.bincount(y_resampled))

# Train the model with resampled data
model = xgb.XGBClassifier(objective='multi:softmax', num_class=len(np.unique(y_resampled)))
model.fit(X_resampled, y_resampled)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Classification report
report = classification_report(y_test, y_pred)
print('Classification Report:')
print(report)