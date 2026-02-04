import sqlite3
import os

def get_db(app):
    os.makedirs("instance", exist_ok=True)
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    conn = get_db(app)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            date TEXT,
            reason TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    """)

    conn.commit()
    conn.close()
