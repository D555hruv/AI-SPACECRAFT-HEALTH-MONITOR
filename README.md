# 🛰️ AI-Based Spacecraft Health Monitoring System

An AI-powered telemetry monitoring system that collects real-time sensor data from an ESP8266-based hardware prototype and uses a Machine Learning model to classify spacecraft health into:

- 🟢 HEALTHY
- 🟡 WARNING
- 🔴 CRITICAL

The system combines embedded hardware, real-time telemetry, data logging, and a Random Forest machine-learning model into a single spacecraft health-monitoring pipeline.

---

## 🚀 Project Overview

Spacecraft operate in harsh environments where continuous monitoring of onboard systems is essential.

This project demonstrates a prototype spacecraft health-monitoring system capable of:

1. Collecting sensor telemetry from an ESP8266.
2. Reading temperature and humidity.
3. Detecting light conditions.
4. Measuring acceleration.
5. Measuring angular velocity.
6. Transmitting telemetry through serial communication.
7. Feeding sensor data into a Machine Learning model.
8. Predicting spacecraft health.
9. Calculating prediction confidence.
10. Saving live telemetry for analysis.
11. Displaying the system through a Streamlit dashboard.

---

## 🧠 Artificial Intelligence

The project uses a **Random Forest Classifier** for spacecraft health classification.

### Health Classes

| Class | Meaning |
|---|---|
| HEALTHY | Spacecraft parameters are within the learned normal range |
| WARNING | Parameters indicate an abnormal condition |
| CRITICAL | Parameters indicate a severe abnormal condition |

The training dataset contains:

- 1000 HEALTHY samples
- 1000 WARNING samples
- 1000 CRITICAL samples

**Total: 3000 samples**

---

## 📊 Machine Learning Results

The Random Forest model was trained using:

- Training samples: 2400
- Testing samples: 600

### Test Accuracy

**100.00%**

Classification results:

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| CRITICAL | 1.00 | 1.00 | 1.00 |
| HEALTHY | 1.00 | 1.00 | 1.00 |
| WARNING | 1.00 | 1.00 | 1.00 |

The confusion matrix produced:

```text
[[200   0   0]
 [  0 200   0]
# 🛰️ AI-Based Spacecraft Health Monitoring System

An AI-powered telemetry monitoring system that collects real-time sensor data from an ESP8266-based hardware prototype and uses a Machine Learning model to classify spacecraft health into:

- 🟢 HEALTHY
- 🟡 WARNING
- 🔴 CRITICAL

The system combines embedded hardware, real-time telemetry, data logging, and a Random Forest machine-learning model into a single spacecraft health-monitoring pipeline.

---

## 🚀 Project Overview

Spacecraft operate in harsh environments where continuous monitoring of onboard systems is essential.

This project demonstrates a prototype spacecraft health-monitoring system capable of:

1. Collecting sensor telemetry from an ESP8266.
2. Reading temperature and humidity.
3. Detecting light conditions.
4. Measuring acceleration.
5. Measuring angular velocity.
6. Transmitting telemetry through serial communication.
7. Feeding sensor data into a Machine Learning model.
8. Predicting spacecraft health.
9. Calculating prediction confidence.
10. Saving live telemetry for analysis.
11. Displaying the system through a Streamlit dashboard.

---

## 🧠 Artificial Intelligence

The project uses a **Random Forest Classifier** for spacecraft health classification.

### Health Classes

| Class | Meaning |
|---|---|
| HEALTHY | Spacecraft parameters are within the learned normal range |
| WARNING | Parameters indicate an abnormal condition |
| CRITICAL | Parameters indicate a severe abnormal condition |

The training dataset contains:

- 1000 HEALTHY samples
- 1000 WARNING samples
- 1000 CRITICAL samples

**Total: 3000 samples**

---

## 📊 Machine Learning Results

The Random Forest model was trained using:

- Training samples: 2400
- Testing samples: 600

### Test Accuracy

**100.00%**

Classification results:

| Class | Precision | Recall | F1-score |
|---|---:|---:|---:|
| CRITICAL | 1.00 | 1.00 | 1.00 |
| HEALTHY | 1.00 | 1.00 | 1.00 |
| WARNING | 1.00 | 1.00 | 1.00 |

The confusion matrix produced:

```text
[[200   0   0]
 [  0 200   0]
 [  0   0 200]]
