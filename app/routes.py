from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = "supersecretkey"


DB = "mydatabase.db"


def get_db():
return sqlite3.connect(DB)


@app.route("/")
def home():
return render_template("home.html")


@app.route("/patient", methods=["GET", "POST"])
def patient_login():
if request.method == "POST":
username = request.form["username"]
password = request.form["password"]


conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
user = cursor.fetchone()
conn.close()


if user and check_password_hash(user[1], password):
session["user_id"] = user[0]
session["username"] = username
return redirect(url_for("welcome"))


return "Invalid credentials"


return render_template("patient_login.html")


@app.route("/welcome")
def welcome():
if "username" not in session:
return redirect(url_for("patient_login"))
return render_template("welcome.html", username=session["username"])


@app.route("/personal-info")
def personal_info():
return render_template("personal_info.html")


@app.route("/schedule")
def schedule():
return render_template("schedule.html")


@app.route("/logout")
def logout():
session.clear()
return redirect(url_for("home"))


if __name__ == "__main__":
app.run(debug=True)
