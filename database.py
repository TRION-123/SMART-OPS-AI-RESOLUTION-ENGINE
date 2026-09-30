import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect("smartops.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motor_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            current REAL,
            vibration REAL,
            voltage REAL,
            power REAL,
            rpm INTEGER,
            motor_status TEXT,
            fault TEXT,
            relay TEXT,
            buzzer TEXT,
            ai_prediction TEXT,
            health_score REAL
        )
    """)

    conn.commit()
    conn.close()


def save_event(
    temperature,
    current,
    vibration,
    voltage,
    power,
    rpm,
    motor_status,
    fault,
    relay,
    buzzer,
    ai_prediction,
    health_score
):

    conn = sqlite3.connect("smartops.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO motor_events (
            timestamp,
            temperature,
            current,
            vibration,
            voltage,
            power,
            rpm,
            motor_status,
            fault,
            relay,
            buzzer,
            ai_prediction,
            health_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        temperature,
        current,
        vibration,
        voltage,
        power,
        rpm,
        motor_status,
        fault,
        relay,
        buzzer,
        ai_prediction,
        health_score
    ))

    conn.commit()
    conn.close()