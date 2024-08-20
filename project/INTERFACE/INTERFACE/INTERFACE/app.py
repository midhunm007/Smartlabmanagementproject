from turtle import pd
from flask import Flask, request, redirect, url_for, jsonify
import pandas as pd
import mysql.connector
from flask import url_for
from flask import session, render_template


app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
    try:
        user = session['username']
        return redirect('admin')
    except:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if role == 'student':
            cursor.execute('SELECT * FROM student WHERE sid = %s AND spd = %s', (username, password))
            student = cursor.fetchone()

            if student:
                # Store the student ID in the session
                session['username'] = student[0]
                # session.permanent()
                # Redirect to student dashboard
                return redirect(url_for('student_dashboard'))

        elif role == 'teacher':
            cursor.execute('SELECT * FROM teacher WHERE tid = %s AND tpd = %s', (username, password))
            teacher = cursor.fetchone()

            if teacher:
                # Store the teacher ID in the session
                session['username'] = teacher[0]
                # Redirect to teacher dashboard
                return redirect(url_for('teacher_dashboard'))

        elif role == 'admin':
            cursor.execute('SELECT * FROM admin WHERE aid = %s AND apd = %s', (username, password))
            admin = cursor.fetchone()

            if admin:
                # Store the admin ID in the session
                session['username'] = admin[0]
                # Redirect to admin dashboard
                print("Here")
                return redirect(url_for('admin_dashboard'))

        else:
            # If the role is not recognized, return an error message
            return render_template('error.html', message='Invalid role')

    else:
        return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    # Fetch existing data for classes, students, and teachers
    cursor.execute('SELECT * FROM class')
    classes = cursor.fetchall()

    cursor.execute('SELECT * FROM student')
    students = cursor.fetchall()

    cursor.execute('SELECT * FROM teacher')
    teachers = cursor.fetchall()

    return render_template('admin_dashboard.html', classes=classes, students=students, teachers=teachers)


@app.route('/teacher')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')



@app.route('/labcycles')
def labcycles():
    return render_template('labcycles.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/submit_class/<id>/<branch>/<int:year>/<section>', methods=['POST'])
def submit_class(id, branch, year, section):
    try:
        # Insert the new class data into the database
        cursor.execute("INSERT INTO class (cid, depid, yid, section) VALUES (%s, %s, %s, %s)", (id, branch, year, section))
        db.commit()
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        print(e)
        db.rollback()
        return jsonify({'error': 'Failed to add class'}), 500



@app.route('/submit_student/<id>/<password>/<name>/<rollno>/<branch>/<int:year>/<section>/<email>', methods=['POST'])
def submit_student(id, password, name, rollno, branch, year, section, email):
    try:
        # Insert the new student data into the database
        cursor.execute("INSERT INTO student (sid, spd, sname, rollno, depid, yid, section, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, password, name, rollno, branch, year, section, email))
        db.commit()
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        print(e)  # Print the error message to aid debugging
        db.rollback()
        return jsonify({'error': 'Failed to add student'}), 500

# Route to handle submitting new teacher data
@app.route('/submit_teacher/<id>/<password>/<name>/<department>/<email>', methods=['POST'])
def submit_teacher(id, password, name, department, email):
    
    try:   
         # Insert the new teacher data into the database
        cursor.execute("INSERT INTO teacher (tid, tpd, tname, depid, email) VALUES (%s, %s, %s, %s, %s)", (id, password, name, department, email))
        db.commit()
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        print(e)
        db.rollback()
        return jsonify({'error': 'Failed to add teacher'}), 500
    

@app.route('/update_class/<id>/<branch>/<int:year>/<section>', methods=['POST'])
def update_class(id, branch, year, section):
    if request.method == 'POST':
        try:
            # Update the class record in the database
            cursor.execute("UPDATE class SET depid = %s, yid = %s, section = %s WHERE cid = %s", (branch, year, section, id))
            db.commit()
            return 'Class record updated successfully', 200
        except Exception as e:
            print(e)
            db.rollback()
            return f'Failed to update class record: {str(e)}', 500
        


@app.route('/update_teacher/<id>/<password>/<name>/<department>/<email>', methods=['POST'])
def update_teacher(id, password, name, department, email):
    if request.method == 'POST':
        
        # Update the teacher record in the database
        try:
            cursor.execute('UPDATE teacher SET tname = %s, depid = %s,tpd = %s, email = %s WHERE tid = %s', (name, department, password, email, id))
            db.commit()
            return 'Teacher record updated successfully', 200
        except Exception as e:
            db.rollback()
            return f'Failed to update teacher record: {str(e)}', 500


@app.route('/update_student/<id>/<password>/<name>/<rollno>/<branch>/<int:year>/<section>/<email>', methods=['POST'])
def update_student(id, password, name, rollno, branch, year, section, email):
    if request.method == 'POST':
        
        
        # Update the student record in the database
        try:
            cursor.execute('UPDATE student SET sname = %s, rollno = %s, depid = %s, yid = %s, section = %s, spd = %s, email = %s WHERE sid = %s', (name, rollno, branch, year, section, password, email, id))
            db.commit()
            return 'Student record updated successfully', 200
        except Exception as e:
            db.rollback()
            return f'Failed to update student record: {str(e)}', 500


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file
        file.save('uploads/' + file.filename)

        # Log the filename and size
        app.logger.info(f'File "{file.filename}" uploaded successfully. Size: {len(file.read())} bytes')

        # Process the Excel file
        df = pd.read_excel('uploads/' + file.filename)
        # Assuming the Excel file has columns: ID, Password, Name, Roll No, Branch, Year, Section, Email
        for index, row in df.iterrows():
            # Extract data from the DataFrame
            id = row['ID']
            password = row['Password']
            name = row['Name']
            rollno = row['Roll No']
            branch = row['Branch']
            year = row['Year']
            section = row['Section']
            email = row['Email']

            # Insert data into the database
            query = """
                INSERT INTO student (sid, spd, sname, rollno, depid, yid, section, email) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id, password, name, rollno, branch, year, section, email))
            db.commit()

        # Commit changes and close the database connection
        
        #cursor.close()
       # db.close()

        return jsonify({'message': 'File uploaded successfully'})
    @app.route('/')
    def index():
     return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload File</title>
    </head>
    <body>
        <input type="file" id="fileInput">
        <button id="uploadButton">Upload</button>

        <script>
            document.getElementById('uploadButton').addEventListener('click', function() {
                var fileInput = document.getElementById('fileInput');
                var file = fileInput.files[0];

                if (!file) {
                    alert('Please select a file.');
                    return;
                }

                var formData = new FormData();
                formData.append('file', file);

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (response.ok) {
                        alert('File uploaded successfully.');
                    } else {
                        throw new Error('Failed to upload file.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while uploading the file.');
                });
            });
        </script>
    </body>
    </html>
    """
    
# Route to handle deleting a row (class, student, or teacher)
@app.route('/delete_row/<table>/<id>', methods=['POST'])
def delete_row(table, id):
    if table == 'class':
        cursor.execute("DELETE FROM class WHERE cid = %s", (id,))
    elif table == 'student':
        cursor.execute("DELETE FROM student WHERE sid = %s", (id,))
    elif table == 'teacher':
        cursor.execute("DELETE FROM teacher WHERE tid = %s", (id,))
    else:
        return jsonify({'error': 'Invalid table name'})
    
    db.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/student_dashboard')
def student_dashboard():
    # Assuming you have stored the logged-in student's ID in session['user_id']
    student_id = session.get('username')  # Retrieve the logged-in student's ID from session

    if student_id is None or student_id == '':
        # If student_id is not found in the session, return an error message or redirect to the login page
        return render_template('error.html', message='Student ID not found in session')

    # Fetch student data from the database using the student ID
    cursor.execute('SELECT * FROM student WHERE sid = %s', (student_id,))
    student = cursor.fetchone()

    if student:
        # Fetch class ID using department ID (depid), year ID (yid), and section
        cursor.execute('''
            SELECT cid 
            FROM class 
            WHERE depid = %s AND yid = %s AND section = %s
        ''', (student[4], student[5], student[6]))  # Use the correct indices here
        class_id = cursor.fetchone()

        if class_id:
            # Fetch labs assigned to the class of the logged-in student using the obtained class ID
            cursor.execute('''
                SELECT lab.lname
                FROM lab
                INNER JOIN class ON lab.cid = class.cid
                WHERE class.cid = %s
            ''', (class_id[0],))
            labs = cursor.fetchall()

            return render_template('student_dashboard.html', labs=labs)
        else:
            # If class ID is not found, return an error message
            return render_template('error.html', message='Class ID not found')
    else:
        # If student data is not found, return an error message
        return render_template('error.html', message='Student data not found')



if __name__ == '__main__':
    app.run(debug=True)
