import pandas as pd
import numpy as np

np.random.seed(42)

data = []

# NORMAL
for i in range(200):
    temperature = np.random.normal(40, 4)
    current = np.random.normal(1.2, 0.25)
    vibration = np.random.normal(2, 0.5)
    voltage = np.random.normal(12, 0.2)
    rpm = np.random.normal(1450, 50)
    data.append([temperature, current, vibration, voltage, rpm, "NORMAL"])

# OVERHEATING
for i in range(200):
    temperature = np.random.normal(68, 5)
    current = np.random.normal(1.5, 0.3)
    vibration = np.random.normal(2.5, 0.6)
    voltage = np.random.normal(11.8, 0.2)
    rpm = np.random.normal(1350, 60)
    data.append([temperature, current, vibration, voltage, rpm, "OVERHEATING"])

# OVERLOAD
for i in range(200):
    temperature = np.random.normal(50, 5)
    current = np.random.normal(3.2, 0.4)
    vibration = np.random.normal(3.5, 0.7)
    voltage = np.random.normal(11.5, 0.3)
    rpm = np.random.normal(1150, 80)
    data.append([temperature, current, vibration, voltage, rpm, "OVERLOAD"])

# MECHANICAL FAULT
for i in range(200):
    temperature = np.random.normal(45, 5)
    current = np.random.normal(1.5, 0.3)
    vibration = np.random.normal(6.5, 1)
    voltage = np.random.normal(11.8, 0.2)
    rpm = np.random.normal(1200, 100)
    data.append([temperature, current, vibration, voltage, rpm, "MECHANICAL_FAULT"])

# CRITICAL
for i in range(200):
    temperature = np.random.normal(82, 5)
    current = np.random.normal(4.2, 0.5)
    vibration = np.random.normal(8, 1)
    voltage = np.random.normal(11, 0.4)
    rpm = np.random.normal(900, 100)
    data.append([temperature, current, vibration, voltage, rpm, "CRITICAL"])


columns = [
    "temperature",
    "current",
    "vibration",
    "voltage",
    "rpm",
    "label"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/motor_data.csv", index=False)

print("Dataset created successfully!")
print("Total samples:", len(df))
print(df.head())