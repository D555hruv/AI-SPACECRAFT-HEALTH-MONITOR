import numpy as np
import pandas as pd
import os

np.random.seed(42)

samples_per_class = 1000
data = []

# HEALTHY
for _ in range(samples_per_class):
    temperature = np.random.uniform(20, 35)
    humidity = np.random.uniform(40, 80)
    light = np.random.randint(0, 2)

    accel_x = np.random.normal(0, 1000)
    accel_y = np.random.normal(0, 1000)
    accel_z = np.random.normal(16384, 1000)

    gyro_x = np.random.normal(0, 200)
    gyro_y = np.random.normal(0, 200)
    gyro_z = np.random.normal(0, 200)

    data.append([
        temperature, humidity, light,
        accel_x, accel_y, accel_z,
        gyro_x, gyro_y, gyro_z,
        "HEALTHY"
    ])


# WARNING
for _ in range(samples_per_class):
    temperature = np.random.uniform(40, 60)
    humidity = np.random.uniform(75, 95)
    light = np.random.randint(0, 2)

    accel_x = np.random.normal(0, 2500)
    accel_y = np.random.normal(0, 2500)
    accel_z = np.random.normal(16384, 2500)

    gyro_x = np.random.normal(0, 700)
    gyro_y = np.random.normal(0, 700)
    gyro_z = np.random.normal(0, 700)

    data.append([
        temperature, humidity, light,
        accel_x, accel_y, accel_z,
        gyro_x, gyro_y, gyro_z,
        "WARNING"
    ])


# CRITICAL
for _ in range(samples_per_class):
    temperature = np.random.uniform(65, 90)
    humidity = np.random.uniform(85, 100)
    light = np.random.randint(0, 2)

    accel_x = np.random.normal(0, 6000)
    accel_y = np.random.normal(0, 6000)
    accel_z = np.random.normal(16384, 6000)

    gyro_x = np.random.normal(0, 2000)
    gyro_y = np.random.normal(0, 2000)
    gyro_z = np.random.normal(0, 2000)

    data.append([
        temperature, humidity, light,
        accel_x, accel_y, accel_z,
        gyro_x, gyro_y, gyro_z,
        "CRITICAL"
    ])


columns = [
    "temperature",
    "humidity",
    "light",
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "health"
]

df = pd.DataFrame(data, columns=columns)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

os.makedirs("data", exist_ok=True)

df.to_csv(
    "data/training_dataset.csv",
    index=False
)

print("Training dataset created successfully!")
print()
print("Total samples:", len(df))
print()
print("Health distribution:")
print(df["health"].value_counts())
print()
print("Saved to: data/training_dataset.csv")

