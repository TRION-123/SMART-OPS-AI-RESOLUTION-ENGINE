import streamlit as st
import joblib
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from database import create_database, save_event
create_database()

# -----------------------------
# LOAD AI MODEL
# -----------------------------
model = joblib.load("ai/model/motor_fault_model.pkl")

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="SMARTOPS AI",
    page_icon="⚙️",
    layout="wide"
)

# -----------------------------
# PROFESSIONAL DASHBOARD STYLE
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

h1, h2, h3 {
    font-weight: 700;
}

[data-testid="stMetric"] {
    background-color: #1a1f2b;
    border: 1px solid #303642;
    padding: 15px;
    border-radius: 10px;
}

[data-testid="stSidebar"] {
    background-color: #151922;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ SMARTOPS AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Live Monitoring",
        "AI Analysis",
        "Fault Detection",
        "Event History"
    ]
)

st.sidebar.divider()

st.sidebar.write("SYSTEM STATUS")
st.sidebar.success("● SYSTEM ONLINE")
st.sidebar.write("Mode: SIMULATION")
st.sidebar.write("Controller: STM32")

st.sidebar.divider()

st.sidebar.subheader("Fault Simulation")

fault_mode = st.sidebar.selectbox(
    "Select Motor Condition",
    [
        "NORMAL",
        "OVERHEATING",
        "OVERLOAD",
        "MECHANICAL FAULT",
        "CRITICAL"
    ]
)

# -----------------------------
# SENSOR SIMULATION
# -----------------------------

if fault_mode == "NORMAL":

    temperature = round(random.uniform(35, 50), 2)
    current = round(random.uniform(0.8, 2.0), 2)
    vibration = round(random.uniform(1, 3), 2)
    voltage = round(random.uniform(11.8, 12.4), 2)
    rpm = random.randint(1400, 1500)

elif fault_mode == "OVERHEATING":

    temperature = round(random.uniform(65, 75), 2)
    current = round(random.uniform(1.2, 2.0), 2)
    vibration = round(random.uniform(1, 3), 2)
    voltage = round(random.uniform(11.8, 12.2), 2)
    rpm = random.randint(1300, 1450)

elif fault_mode == "OVERLOAD":

    temperature = round(random.uniform(45, 60), 2)
    current = round(random.uniform(3.0, 4.0), 2)
    vibration = round(random.uniform(2, 4), 2)
    voltage = round(random.uniform(11.5, 12.0), 2)
    rpm = random.randint(1100, 1300)

elif fault_mode == "MECHANICAL FAULT":

    temperature = round(random.uniform(40, 55), 2)
    current = round(random.uniform(1.0, 2.0), 2)
    vibration = round(random.uniform(6, 8), 2)
    voltage = round(random.uniform(11.8, 12.2), 2)
    rpm = random.randint(1000, 1300)

else:

    temperature = round(random.uniform(76, 90), 2)
    current = round(random.uniform(4.0, 5.0), 2)
    vibration = round(random.uniform(8, 10), 2)
    voltage = round(random.uniform(10.5, 11.5), 2)
    rpm = random.randint(700, 1000)

power = round(voltage * current, 2)

# -----------------------------
# AI PREDICTION
# -----------------------------

data = pd.DataFrame(
    [[
        temperature,
        current,
        vibration,
        voltage,
        rpm
    ]],
    columns=[
        "temperature",
        "current",
        "vibration",
        "voltage",
        "rpm"
    ]
)

prediction = model.predict(data)[0]

probabilities = model.predict_proba(data)[0]

confidence = max(probabilities) * 100

# -----------------------------
# MOTOR PROTECTION
# -----------------------------

if fault_mode in [
    "OVERLOAD",
    "MECHANICAL FAULT",
    "CRITICAL"
]:

    motor_status = "STOPPED"
    relay_status = "OFF"
    buzzer_status = "ON"
    protection_status = "FAULT - MOTOR SHUTDOWN"

elif fault_mode == "OVERHEATING":

    motor_status = "RUNNING"
    relay_status = "ON"
    buzzer_status = "OFF"
    protection_status = "WARNING - OVERHEATING"

else:

    motor_status = "RUNNING"
    relay_status = "ON"
    buzzer_status = "OFF"
    protection_status = "NORMAL"


# -----------------------------
# HEALTH SCORE
# -----------------------------

if fault_mode == "NORMAL":
    health_score = 100

elif fault_mode == "OVERHEATING":
    health_score = 75

elif fault_mode == "OVERLOAD":
    health_score = 55

elif fault_mode == "MECHANICAL FAULT":
    health_score = 50

else:
    health_score = 25


# -----------------------------
# SAVE MOTOR EVENT
# -----------------------------

save_event(
    temperature,
    current,
    vibration,
    voltage,
    power,
    rpm,
    motor_status,
    fault_mode,
    relay_status,
    buzzer_status,
    prediction,
    health_score
)

# -----------------------------
# HEADER
# -----------------------------

st.title("⚙️ SMARTOPS AI")

st.caption(
    "INDUSTRIAL MOTOR MONITORING & FAULT DETECTION"
)

st.divider()

# ==================================================
# OVERVIEW
# ==================================================

if page == "Overview":

    st.header("Motor Overview")

    st.write(
        "Last Updated:",
        datetime.now().strftime("%H:%M:%S")
    )

    st.divider()

    # SENSOR CARDS

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡 Temperature",
        f"{temperature} °C"
    )

    col2.metric(
        "⚡ Current",
        f"{current} A"
    )

    col3.metric(
        "〽 Vibration",
        f"{vibration}"
    )

    col4.metric(
        "🔌 Voltage",
        f"{voltage} V"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "⚙ RPM",
        rpm
    )

    col2.metric(
        "🔋 Power",
        f"{power} W"
    )

    col3.metric(
        "🤖 AI Confidence",
        f"{confidence:.1f}%"
    )

    col4.metric(
        "🏭 Motor",
        motor_status
    )

    st.divider()

    # PROTECTION STATUS

    st.subheader("⚡ Motor Protection Status")

    col1, col2, col3 = st.columns(3)

    col1.metric("Motor", motor_status)

    col2.metric("Relay", relay_status)

    col3.metric("Buzzer", buzzer_status)

    if fault_mode == "NORMAL":

        st.success(
            "🟢 SYSTEM NORMAL — MOTOR RUNNING"
        )

    elif fault_mode == "OVERHEATING":

        st.warning(
            "🟡 WARNING — MOTOR OVERHEATING"
        )

    else:

        st.error(
            f"🔴 {fault_mode} — MOTOR SHUTDOWN"
        )

    st.divider()

    # AI RESULT

    st.subheader("🤖 AI Prediction")

    col1, col2 = st.columns(2)

    col1.info(
        f"Predicted Condition: **{prediction}**"
    )

    col2.info(
        f"AI Confidence: **{confidence:.2f}%**"
    )


# ==================================================
# LIVE MONITORING
# ==================================================

elif page == "Live Monitoring":
    st_autorefresh(interval=2000, key="motor_refresh")

    st.header("📊 Live Motor Monitoring")

    st.write(
        "Real-time simulated sensor values"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Temperature",
        f"{temperature} °C"
    )

    col2.metric(
        "Current",
        f"{current} A"
    )

    col3.metric(
        "Vibration",
        f"{vibration}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Voltage",
        f"{voltage} V"
    )

    col2.metric(
        "Power",
        f"{power} W"
    )

    col3.metric(
        "RPM",
        rpm
    )

    st.divider()

    st.subheader("📈 Real-Time Sensor Trends")

    history = pd.DataFrame({
        "Time": range(30),
        "Temperature": [
            temperature + random.uniform(-3, 3)
            for _ in range(30)
        ],
        "Current": [
            current + random.uniform(-0.2, 0.2)
            for _ in range(30)
        ],
        "Vibration": [
            vibration + random.uniform(-0.5, 0.5)
            for _ in range(30)
        ]
    })

    history = history.set_index("Time")

    st.line_chart(
        history[
            ["Temperature", "Current", "Vibration"]
        ]
    )

# ==================================================
# AI ANALYSIS
# ==================================================

elif page == "AI Analysis":

    st.header("🤖 AI Motor Analysis")

    st.write("Random Forest based motor fault classification")

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "Predicted Condition",
        prediction
    )

    col2.metric(
        "AI Confidence",
        f"{confidence:.2f}%"
    )

    st.divider()

    st.subheader("Sensor Data Used by AI")

    st.dataframe(
        data,
        use_container_width=True
    )


# ==================================================
# FAULT DETECTION
# ==================================================

elif page == "Fault Detection":

    st.header("🚨 Fault Detection")

    st.write(
        "Motor protection and fault status"
    )

    st.divider()

    st.metric(
        "Selected Fault",
        fault_mode
    )

    st.metric(
        "AI Prediction",
        prediction
    )

    st.divider()

    st.subheader("Protection System")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Motor",
        motor_status
    )

    col2.metric(
        "Relay",
        relay_status
    )

    col3.metric(
        "Buzzer",
        buzzer_status
    )

    st.divider()

    if fault_mode == "NORMAL":

        st.success(
            "🟢 No fault detected. Motor is operating normally."
        )

    elif fault_mode == "OVERHEATING":

        st.warning(
            "🟡 High temperature detected. Monitor motor condition."
        )

    else:

        st.error(
            f"🔴 {fault_mode} detected. Motor has been shut down."
        )

# ==================================================
# EVENT HISTORY
# ==================================================

elif page == "Event History":

    st.header("📋 Motor Event History")

    st.write(
        "Previously recorded motor conditions and fault events"
    )

    st.divider()

    import sqlite3

    conn = sqlite3.connect("smartops.db")

    events = pd.read_sql_query(
        "SELECT * FROM motor_events ORDER BY id DESC",
        conn
    )

    conn.close()

    if events.empty:

        st.info("No motor events recorded yet.")

    else:

        st.subheader("Recent Motor Events")

        st.dataframe(
            events,
            use_container_width=True,
            hide_index=True
        )