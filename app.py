import os
from flask import Flask, render_template, request, redirect, session, flash
from db import get_db_connection
import csv
from flask import Response
app = Flask(__name__)
app.secret_key = "your_secret_key_here"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- ABOUT ----------------
@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- STUDENTS DASHBOARD ----------------
@app.route('/students', methods=['GET', 'POST'])
def students():

    # Login protection
    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Add student
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )

        conn.commit()
        conn.close()

        return redirect('/students')

    # Get students
    cursor.execute("SELECT * FROM students")
    students_list = cursor.fetchall()

    total_students = len(students_list)

    gmail_users = sum(
        1 for student in students_list
        if "@gmail.com" in student["email"].lower()
    )

    non_gmail_users = total_students - gmail_users

    conn.close()

    return render_template(
        'students.html',
        students=students_list,
        total_students=total_students,
        gmail_users=gmail_users,
        non_gmail_users=non_gmail_users,
        total_records=total_students
    )


# ---------------- DELETE STUDENT ----------------
@app.route('/delete/<int:id>')
def delete_student(id):

    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/students')


# ---------------- EDIT STUDENT ----------------
@app.route('/edit/<int:id>')
def edit_student(id):

    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )


# ---------------- UPDATE STUDENT ----------------
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    if not session.get('logged_in'):
        return redirect('/login')

    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=%s,
            email=%s
        WHERE id=%s
        """,
        (name, email, id)
    )

    conn.commit()
    conn.close()

    return redirect('/students')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin:

            session['logged_in'] = True
            session['username'] = username

            flash("Login successful!", "success")

            return redirect('/students')

        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('logged_in', None)
    session.pop('username', None)

    flash("Logged out successfully!", "info")

    return redirect('/login')

# ---------------- EXPORT CSV ----------------
@app.route('/export/csv')
def export_csv():

    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    output = "id,name,email\n"

    for s in students:
        output += f"{s['id']},{s['name']},{s['email']}\n"

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=students.csv"}
    )

# ---------------- TEST DATABASE ----------------
@app.route('/test')
def test():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()

    return str(data)


# ---------------- RUN APP ----------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )