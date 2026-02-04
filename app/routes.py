from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .database import get_db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/patients", methods=["GET", "POST"])
def patients():
    conn = get_db(current_app)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        cursor.execute(
            "INSERT INTO patients (name, phone) VALUES (?, ?)",
            (name, phone)
        )
        conn.commit()

    patients = cursor.execute("SELECT * FROM patients").fetchall()
    conn.close()
    return render_template("patients.html", patients=patients)

@main.route("/appointments", methods=["GET", "POST"])
def appointments():
    conn = get_db(current_app)
    cursor = conn.cursor()

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        date = request.form["date"]
        reason = request.form["reason"]

        cursor.execute(
            "INSERT INTO appointments (patient_id, date, reason) VALUES (?, ?, ?)",
            (patient_id, date, reason)
        )
        conn.commit()

    patients = cursor.execute("SELECT * FROM patients").fetchall()
    appointments = cursor.execute("""
        SELECT a.id, p.name, a.date, a.reason
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
    """).fetchall()

    conn.close()
    return render_template(
        "appointments.html",
        patients=patients,
        appointments=appointments
    )
