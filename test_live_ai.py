import joblib
import pandas as pd

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

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

# ==========================================
# TEST CONDITIONS
# ==========================================

tests = {

    "NORMAL CONDITION": [
        30.8,     # Temperature
        79.0,     # Humidity
        1,        # Light
        3104,     # Accel X
        -1356,    # Accel Y
        15320,    # Accel Z
        -35,      # Gyro X
        -355,     # Gyro Y
        76        # Gyro Z
    ],

    "WARNING CONDITION": [
        55.0,
        85.0,
        1,
        5000,
        -2500,
        14000,
        800,
        -700,
        600
    ],

    "CRITICAL CONDITION": [
        85.0,
        95.0,
        0,
        12000,
        -10000,
        5000,
        3000,
        -3000,
        2500
    ]
}

# ==========================================
# RUN TESTS
# ==========================================

print()
print("==========================================")
print(" AI SPACECRAFT HEALTH TEST")
print("==========================================")

for condition, values in tests.items():

    data = pd.DataFrame(
        [values],
        columns=features
    )

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    confidence = max(probabilities) * 100

    print()
    print("------------------------------------------")
    print(condition)
    print("------------------------------------------")

    print(
        f"Temperature : {values[0]:.2f} °C"
    )

    print(
        f"Humidity    : {values[1]:.2f} %"
    )

    print(
        f"Light       : {values[2]}"
    )

    print(
        f"AI Prediction : {prediction}"
    )

    print(
        f"AI Confidence: {confidence:.2f}%"
    )

print()
print("==========================================")
print(" TEST COMPLETE")
print("==========================================")
