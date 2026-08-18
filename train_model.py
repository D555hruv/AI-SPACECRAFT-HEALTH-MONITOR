import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("data/training_dataset.csv")

# Features
features = [
    "temperature",
    "humidity",
    "light",
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z"
]

X = df[features]
y = df["health"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# Create Random Forest
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print()
print("================================")
print("RANDOM FOREST MODEL")
print("================================")
print(f"Accuracy: {accuracy * 100:.2f}%")

print()
print("Classification Report:")
print(classification_report(y_test, y_pred))

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/health_model.pkl"
)

print()
print("Model saved successfully!")
print("Location: models/health_model.pkl")

