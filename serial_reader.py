import serial
import csv
import os
from datetime import datetime

PORT = "/dev/cu.usbserial-0001"
BAUD_RATE = 9600

CSV_FILE = "data/telemetry.csv"

os.makedirs("data", exist_ok=True)

ser = serial.Serial(PORT, BAUD_RATE, timeout=2)

print("Connected to ESP8266")
print("Collecting telemetry...")
print("Press Ctrl+C to stop.")

file_exists = os.path.exists(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
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
            "gyro_z"
        ])

    while True:

        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        values = line.split(",")

        # We need exactly 9 telemetry values
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
            continue

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            gyro_z
        ])

        file.flush()

        print(
            timestamp,
            "|",
            f"T={temperature}°C",
            f"H={humidity}%",
            f"L={light}",
            f"A=({accel_x},{accel_y},{accel_z})",
            f"G=({gyro_x},{gyro_y},{gyro_z})"
        )