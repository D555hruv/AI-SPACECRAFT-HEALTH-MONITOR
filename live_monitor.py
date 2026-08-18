import serial
import joblib
import pandas as pd
import csv
import os
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "/dev/cu.usbserial-0001"
BAUD_RATE = 9600

LOG_FILE = "data/live_telemetry.csv"

# ==========================================
# LOAD AI MODEL
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
# CREATE DATA DIRECTORY
# ==========================================

os.makedirs("data", exist_ok=True)

# ==========================================
# CREATE CSV FILE + HEADER
# ==========================================

if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:

    with open(LOG_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "temperature",
            "humidity",
            "light",
            "accel_x",
            "accel_y",
            "accel_z",
            "gyro_x",
            "gyro_y",
            "gyro_z",
            "health",
            "confidence"
        ])

# ==========================================
# CONNECT TO ESP8266
# ==========================================

try:

    ser = serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=2
    )

except Exception as e:

    print("ERROR: Could not connect to ESP8266")
    print(e)
    exit()

# ==========================================
# START
# ==========================================

print()
print("==========================================")
print(" AI SPACECRAFT HEALTH MONITOR")
print(" LIVE SENSOR MODE")
print("==========================================")
print("Connected to ESP8266")
print("Collecting telemetry...")
print("Press Ctrl+C to stop.")
print()

# ==========================================
# MAIN LOOP
# ==========================================

try:

    while True:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        # ----------------------------------
        # SPLIT SENSOR DATA
        # ----------------------------------

        values = line.split(",")

        # ESP8266 should send exactly 9 values
        if len(values) != 9:
            continue

        try:

            temperature = float(values[0])
            humidity = float(values[1])
            light = int(values[2])

            accel_x = int(values[3])
            accel_y = int(values[4])
            accel_z = int(values[5])

            gyro_x = int(values[6])
            gyro_y = int(values[7])
            gyro_z = int(values[8])

        except ValueError:

            # Ignore corrupted serial data
            continue

        # ----------------------------------
        # SENSOR VALIDATION
        # ----------------------------------

        if not (0 <= temperature <= 100):
            print(
                "Ignoring invalid temperature:",
                temperature
            )
            continue

        if not (0 <= humidity <= 100):
            print(
                "Ignoring invalid humidity:",
                humidity
            )
            continue

        if light not in [0, 1]:
            print(
                "Ignoring invalid light value:",
                light
            )
            continue

        # ----------------------------------
        # CREATE AI INPUT
        # ----------------------------------

        sensor_data = pd.DataFrame(
            [[
                temperature,
                humidity,
                light,
                accel_x,
                accel_y,
                accel_z,
                gyro_x,
                gyro_y,
                gyro_z
            ]],
            columns=features
        )

        # ----------------------------------
        # AI PREDICTION
        # ----------------------------------

        prediction = model.predict(
            sensor_data
        )[0]

        probabilities = model.predict_proba(
            sensor_data
        )[0]

        confidence = max(
            probabilities
        ) * 100

        # ----------------------------------
        # TIMESTAMP
        # ----------------------------------

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # ----------------------------------
        # DISPLAY
        # ----------------------------------

        print("------------------------------------------")

        print(
            f"Temperature : {temperature:.2f} °C"
        )

        print(
            f"Humidity    : {humidity:.2f} %"
        )

        print(
            f"Light       : {light}"
        )

        print(
            f"Accel       : X={accel_x} "
            f"Y={accel_y} "
            f"Z={accel_z}"
        )

        print(
            f"Gyro        : X={gyro_x} "
            f"Y={gyro_y} "
            f"Z={gyro_z}"
        )

        print()

        print(
            f"SPACECRAFT HEALTH: {prediction}"
        )

        print(
            f"AI CONFIDENCE: {confidence:.2f}%"
        )

        print("------------------------------------------")

        # ----------------------------------
        # SAVE TO CSV
        # ----------------------------------

        with open(
            LOG_FILE,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                temperature,
                humidity,
                light,
                accel_x,
                accel_y,
                accel_z,
                gyro_x,
                gyro_y,
                gyro_z,
                prediction,
                round(confidence, 2)
            ])

except KeyboardInterrupt:

    print()
    print("Stopping telemetry collection...")

finally:

    ser.close()

    print("Serial connection closed.")
    print(
        f"Telemetry saved to: {LOG_FILE}"
    )
