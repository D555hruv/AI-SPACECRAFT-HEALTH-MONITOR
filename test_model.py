import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/health_model.pkl")

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

# Test cases
test_cases = [
    {
        "name": "Normal spacecraft condition",
        "temperature": 30,
        "humidity": 60,
        "light": 1,
        "accel_x": 500,
        "accel_y": -300,
        "accel_z": 16300,
        "gyro_x": 50,
        "gyro_y": -30,
        "gyro_z": 40
    },

    {
        "name": "Warning condition",
        "temperature": 50,
        "humidity": 85,
        "light": 1,
        "accel_x": 2500,
        "accel_y": -1800,
        "accel_z": 18000,
        "gyro_x": 700,
        "gyro_y": 500,
        "gyro_z": -600
    },

    {
        "name": "Critical condition",
        "temperature": 80,
        "humidity": 95,
        "light": 0,
        "accel_x": 7000,
        "accel_y": -6000,
        "accel_z": 22000,
        "gyro_x": 2500,
        "gyro_y": -2000,
        "gyro_z": 1800
    }
]

print("================================")
print("AI SPACECRAFT HEALTH TEST")
print("================================")

for case in test_cases:

    input_data = pd.DataFrame(
        [[case[feature] for feature in features]],
        columns=features
    )

    prediction = model.predict(input_data)[0]

    print()
    print("Test:", case["name"])
    print("Predicted Health:", prediction)

print()
print("================================")
