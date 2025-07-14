import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# 1) Load your dataset
data = pd.read_csv('first inten project.csv')

# Drop ID column if it exists (adjust if different name)
data = data.drop('Booking_ID', axis=1, errors='ignore')

# Encode categorical columns with mapping
meal_map = {'Meal Plan 1': 0, 'Not Selected': 1, 'Meal Plan 2': 2, 'Meal Plan 3': 3}
room_map = {'Room_Type 1': 0, 'Room_Type 4': 1, 'Room_Type 6': 2, 'Room_Type 2': 3, 'Room_Type 5': 4, 'Room_Type 7': 5, 'Room_Type 3': 6}
segment_map = {'Online': 0, 'Offline': 1, 'Corporate': 2, 'Complementary': 3, 'Aviation': 4}

data['type of meal'] = data['type of meal'].map(meal_map)
data['room type'] = data['room type'].map(room_map)
data['market segment type'] = data['market segment type'].map(segment_map)

# Encode date of reservation as day of year
data['date of reservation'] = pd.to_datetime(data['date of reservation'], errors='coerce').dt.dayofyear

# Drop rows with NaN (from date conversion or encoding)
data = data.dropna()

# 2) Select features and target
X = data.drop('booking status', axis=1)
y = data['booking status'].map({'Not_Canceled': 0, 'Canceled': 1})

# 3) Preprocessing (Scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4) Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 5) Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 6) Save Model and Scaler
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Model and Scaler saved successfully.")
