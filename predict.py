import joblib
import pandas as pd

# Load the trained AI model
model = joblib.load("ai/model/motor_fault_model.pkl")

# Enter new motor sensor values
temperature = float(input("Enter temperature (°C): "))
current = float(input("Enter current (A): "))
vibration = float(input("Enter vibration: "))
voltage = float(input("Enter voltage (V): "))
rpm = float(input("Enter RPM: "))

# Create input data
new_data = pd.DataFrame([[
    temperature,
    current,
    vibration,
    voltage,
    rpm
]], columns=[
    "temperature",
    "current",
    "vibration",
    "voltage",
    "rpm"
])

# Predict motor condition
prediction = model.predict(new_data)[0]

# Get prediction probabilities
probabilities = model.predict_proba(new_data)[0]
confidence = max(probabilities) * 100

print("\n---------------------------")
print("SMARTOPS AI RESULT")
print("---------------------------")
print("Motor Condition:", prediction)
print("AI Confidence:", round(confidence, 2), "%")