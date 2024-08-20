from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydb"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('admin.html')

@app.route('/submit_class', methods=['POST'])
def submit_class():
    if request.method == 'POST':
        class_id = request.form['cid']
        department_id = request.form['depid']
        year_id = request.form['yid']
        section = request.form['section']
        cursor.execute("INSERT INTO class (cid, depid, yid, section) VALUES (%s, %s, %s, %s)", (class_id, department_id, year_id, section))
        db.commit()
        return 'Class data submitted successfully'

@app.route('/submit_student', methods=['POST'])
def submit_student():
    if request.method == 'POST':
        student_id = request.form['sid']
        password = request.form['password']
        name = request.form['sname']
        rollno = request.form['rollno']
        department_id = request.form['depid']
        year_id = request.form['yid']
        section = request.form['section']
        email = request.form['email']
        cursor.execute("INSERT INTO student (sid, spd, sname, rollno, depid, yid, section, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (student_id, password, name, rollno, department_id, year_id, section, email))
        db.commit()
        return 'Student data submitted successfully'

@app.route('/submit_teacher', methods=['POST'])
def submit_teacher():
    if request.method == 'POST':
        teacher_id = request.form['tid']
        password = request.form['password']
        name = request.form['tname']
        department_id = request.form['depid']
        email = request.form['email']
        cursor.execute("INSERT INTO teacher (tid, tpd, tname, depid, email) VALUES (%s, %s, %s, %s, %s)", (teacher_id, password, name, department_id, email))
        db.commit()
        return 'Teacher data submitted successfully'

if __name__ == '__main__':
    app.run(debug=True)
