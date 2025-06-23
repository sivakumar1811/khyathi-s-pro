from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ----------- CONFIGURATION -----------
UPLOAD_FOLDER = "static/uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ----------- ROUTES -----------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")

@app.route("/user")
def user_dashboard():
    return render_template("user.html")

@app.route("/worker")
def worker_dashboard():
    return render_template("worker.html")

@app.route("/submit_issue", methods=["POST"])
def submit_issue():
    department = request.form.get("department")
    description = request.form.get("description")
    location = request.form.get("location")
    image = request.files.get("image")

    if image and image.filename != "":
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(filepath)
    else:
        filepath = ""

    # Save to database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (user_id, department_id, description, image_path, location)
        VALUES (?, ?, ?, ?, ?)""",
        (1, get_department_id(department), description, filepath, location)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("user_dashboard"))

# ----------- UTILITY FUNCTIONS -----------

def get_department_id(name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM departments WHERE LOWER(name) = ?", (name.lower(),))
    dept = cursor.fetchone()
    conn.close()
    return dept[0] if dept else None

# ----------- SERVER RUN -----------

if __name__ == "__main__":
    app.run(debug=True)
