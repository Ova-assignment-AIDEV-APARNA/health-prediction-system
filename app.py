import re 
from datetime import datetime
from flask import flash, Response
from flask import Flask, render_template, request, redirect
import sqlite3
import csv
from services.ai_services import predict_health
app = Flask(__name__)
app.secret_key = "secret"

def init_db():
    conn = sqlite3.connect('database.db')

    conn.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT NOT NULL,
        glucose REAL NOT NULL,
        haemoglobin REAL NOT NULL,
        cholesterol REAL NOT NULL,
        remarks TEXT
    )
    """)

    conn.commit()
    conn.close()

# Database Connection Function
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create database and table
init_db()


@app.route('/')
def home():
    
    search = request.args.get('search')

    

    conn = get_db()
    

    if search:

        patients = conn.execute(
            "SELECT * FROM patients WHERE fullname LIKE ?",
            ('%' + search + '%',)
        ).fetchall()

    else:

        patients = conn.execute(
            "SELECT * FROM patients"
        ).fetchall()

    conn.close()
    total_patients = len(patients)
    avg_glucose = 0
    if patients:
        avg_glucose = round(
            sum(patient['glucose'] for patient in patients)
            / len(patients),
            2
        )

    return render_template(
        'dashboard.html',
        patients=patients,
        total_patients=total_patients,
        avg_glucose=avg_glucose
    )
@app.route('/export')
def export_csv():

    conn = get_db()

    patients = conn.execute(
        "SELECT * FROM patients"
    ).fetchall()

    conn.close()

    def generate():

        yield "ID,Full Name,Email,Glucose,Haemoglobin,Cholesterol,Remarks\n"

        for patient in patients:

            yield (
                f"{patient['id']},"
                f"{patient['fullname']},"
                f"{patient['email']},"
                f"{patient['glucose']},"
                f"{patient['haemoglobin']},"
                f"{patient['cholesterol']},"
                f"\"{patient['remarks']}\"\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=patients.csv"
        }
    )
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            flash("Invalid Email Format", "danger")
            return redirect('/add')

        dob_date = datetime.strptime(
            dob,
            "%Y-%m-%d"
        )

        if dob_date.date() > datetime.today().date():
            flash("Date of Birth cannot be in the future", "danger")
            return redirect('/add')

        try:
            glucose = float(glucose)
            haemoglobin = float(haemoglobin)
            cholesterol = float(cholesterol)

        except ValueError:
            flash("Blood values must be numeric", "danger")
            return redirect('/add')

        remarks = predict_health(glucose, haemoglobin, cholesterol)
        conn = get_db()

        conn.execute("""
            INSERT INTO patients
            (
                fullname,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES (?,?,?,?,?,?,?)
        """,
        (
            fullname,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_patient.html')
@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    conn = get_db()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == 'POST':

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        conn.execute("""
        UPDATE patients
        SET
            fullname=?,
            dob=?,
            email=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        """,
        (
            request.form['fullname'],
            request.form['dob'],
            request.form['email'],
            glucose,
            haemoglobin,
            cholesterol,
            remarks,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )

if __name__ == "__main__":
    app.run(debug=True)