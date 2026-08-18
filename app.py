import streamlit as st
import pandas as pd
import joblib
import serial
import time
import os

# ==========================================
# CONFIGURATION
# ==========================================

PORT = "/dev/cu.usbserial-0001"
BAUD_RATE = 9600
LOG_FILE = "data/live_telemetry.csv"

FEATURES = [
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
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Spacecraft Health Monitor",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("🚀 AI Spacecraft Health Monitoring System")
st.caption(
    "ESP8266 • DHT11 • HW-072 • MPU-6500 • Random Forest AI"
)

st.divider()

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/health_model.pkl")


model = load_model()

# ==========================================
# SERIAL CONNECTION
# ==========================================

@st.cache_resource
def connect_serial():
    return serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=0.2
    )


try:
    ser = connect_serial()
    connection_status = True
except Exception:
    ser = None
    connection_status = False

# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "latest" not in st.session_state:
    st.session_state.latest = None

# ==========================================
# READ TELEMETRY
# ==========================================

if ser is not None:

    latest_line = None

    while ser.in_waiting > 0:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if line:
            latest_line = line

    if latest_line:

        values = latest_line.split(",")

        if len(values) == 9:

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

                # Validate
                if (
                    0 <= temperature <= 100
                    and
                    0 <= humidity <= 100
                    and
                    light in [0, 1]
                ):

                    sensor_df = pd.DataFrame(
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
                        columns=FEATURES
                    )

                    prediction = model.predict(
                        sensor_df
                    )[0]

                    probabilities = model.predict_proba(
                        sensor_df
                    )[0]

                    confidence = (
                        max(probabilities) * 100
                    )

                    timestamp = time.strftime(
                        "%H:%M:%S"
                    )

                    latest = {
                        "time": timestamp,
                        "temperature": temperature,
                        "humidity": humidity,
                        "light": light,
                        "accel_x": accel_x,
                        "accel_y": accel_y,
                        "accel_z": accel_z,
                        "gyro_x": gyro_x,
                        "gyro_y": gyro_y,
                        "gyro_z": gyro_z,
                        "health": prediction,
                        "confidence": confidence
                    }

                    st.session_state.latest = latest

                    st.session_state.history.append(
                        latest
                    )

                    st.session_state.history = (
                        st.session_state.history[-50:]
                    )

            except ValueError:
                pass

# ==========================================
# CONNECTION STATUS
# ==========================================

if connection_status:

    st.success(
        "🟢 ESP8266 CONNECTION: ACTIVE"
    )

else:

    st.error(
        "🔴 ESP8266 CONNECTION: NOT AVAILABLE"
    )

    st.info(
        "Close Arduino Serial Monitor and make sure "
        "the ESP8266 is connected."
    )

# ==========================================
# LATEST DATA
# ==========================================

data = st.session_state.latest

if data is None:

    st.warning(
        "⏳ Waiting for telemetry from ESP8266..."
    )

else:

    # ======================================
    # HEALTH STATUS
    # ======================================

    health = data["health"]
    confidence = data["confidence"]

    st.subheader("🤖 AI Spacecraft Health Status")

    if health == "HEALTHY":

        st.success(
            f"🟢 HEALTHY   |   "
            f"AI CONFIDENCE: {confidence:.2f}%"
        )

    elif health == "WARNING":

        st.warning(
            f"🟡 WARNING   |   "
            f"AI CONFIDENCE: {confidence:.2f}%"
        )

    else:

        st.error(
            f"🔴 CRITICAL   |   "
            f"AI CONFIDENCE: {confidence:.2f}%"
        )

    # ======================================
    # MAIN SENSOR CARDS
    # ======================================

    st.subheader("📡 Live Telemetry")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🌡️ Temperature",
            f"{data['temperature']:.2f} °C"
        )

    with c2:

        st.metric(
            "💧 Humidity",
            f"{data['humidity']:.2f} %"
        )

    with c3:

        light_text = (
            "Detected"
            if data["light"] == 1
            else "Not Detected"
        )

        st.metric(
            "💡 Light",
            light_text
        )

    with c4:

        st.metric(
            "🕐 Last Update",
            data["time"]
        )

    # ======================================
    # ACCELEROMETER
    # ======================================

    st.subheader("📐 MPU-6500 Accelerometer")

    a1, a2, a3 = st.columns(3)

    with a1:
        st.metric("X Axis", data["accel_x"])

    with a2:
        st.metric("Y Axis", data["accel_y"])

    with a3:
        st.metric("Z Axis", data["accel_z"])

    # ======================================
    # GYROSCOPE
    # ======================================

    st.subheader("🔄 MPU-6500 Gyroscope")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.metric("X Axis", data["gyro_x"])

    with g2:
        st.metric("Y Axis", data["gyro_y"])

    with g3:
        st.metric("Z Axis", data["gyro_z"])

    # ======================================
    # LIVE GRAPHS
    # ======================================

    if len(st.session_state.history) > 1:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.divider()

        st.subheader("📈 Live Sensor Trends")

        # Temperature
        st.write("Temperature")

        st.line_chart(
            history_df.set_index("time")[
                ["temperature"]
            ]
        )

        # Humidity
        st.write("Humidity")

        st.line_chart(
            history_df.set_index("time")[
                ["humidity"]
            ]
        )

        # Accelerometer
        st.write("Accelerometer")

        st.line_chart(
            history_df.set_index("time")[
                [
                    "accel_x",
                    "accel_y",
                    "accel_z"
                ]
            ]
        )

        # Gyroscope
        st.write("Gyroscope")

        st.line_chart(
            history_df.set_index("time")[
                [
                    "gyro_x",
                    "gyro_y",
                    "gyro_z"
                ]
            ]
        )

        # ==================================
        # RECENT DATA
        # ==================================

        st.subheader("📊 Recent Telemetry")

        display_df = history_df.tail(10).copy()

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# SAVED DATA
# ==========================================

st.divider()

st.subheader("💾 Recorded Telemetry")

if os.path.exists(LOG_FILE):

    saved_df = pd.read_csv(LOG_FILE)

    if len(saved_df) > 0:

        st.write(
            f"Total recorded readings: "
            f"**{len(saved_df)}**"
        )

        st.download_button(
            label="📥 Download Telemetry CSV",
            data=saved_df.to_csv(index=False),
            file_name="spacecraft_telemetry.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No telemetry has been permanently recorded yet."
        )

else:

    st.info(
        "live_telemetry.csv has not been created yet."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI-Based Spacecraft Health Monitoring Platform | "
    "ESP8266 + Multi-Sensor Telemetry + Random Forest"
)

# ==========================================
# AUTO REFRESH
# ==========================================

time.sleep(2)
st.rerun()
