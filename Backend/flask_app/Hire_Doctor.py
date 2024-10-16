from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector as myc
import random
from datetime import datetime  # For getting the current date

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


def generate_doctor_id():
    a = random.choice('ABCDEFGHIJKLmnopqrstuvwxyz')
    b = random.choice('1234567890')
    c = random.choice('1234567890')
    d = random.choice('1234567890')
    return str(a) + str(b) + str(c) + str(d)

@app.route('/Hire_Doctor', methods=['POST'])
def hire():
    db = None
    cur = None
    try:
        # Retrieve data from the request body
        data = request.get_json()
        Doctor_Name = data.get('fullName')  # Match the name field from frontend
        mobile_no = data.get('mobile_no')
        Gender = data.get('gender')
        Specialisation = data.get('specialisation')
        Working_Hrs = data.get('working_hrs')  # New field
        Age = data.get('age')
        Salary = data.get('salary')
        Fees = data.get('fees')
        username = data.get('username')
        Passwd = data.get('password')

        # Validate input data
        if not all([Doctor_Name, mobile_no, Gender, Specialisation, Working_Hrs, Age, Salary, Fees,username, Passwd]):
            return jsonify({'error': 'All fields are required'}), 400

        if len(Passwd) <= 5:
            return jsonify({'error': 'Password must be min 5 characters long'}), 400

        # Connect to the database
        db = myc.connect(host='localhost', user='root', port='3306', passwd='mysql123', database='micro_project')
        cur = db.cursor()

        # Generate parking ID and insert into Parking table
        park_id = generate_park_id()
        cur.execute("INSERT INTO Parking (park_id, owner) VALUES (%s, %s)", (park_id, Doctor_Name))

        # Insert login credentials into the login table
        dt_admit = datetime.now().strftime('%Y-%m-%d')  # Get current date
        cur.execute("INSERT INTO login (username, pwd, role, last_login) VALUES (%s, %s, %s, %s)", 
                    (username, Passwd, 'DOCTOR', dt_admit))

        # Generate a doctor ID
        dr_id = generate_doctor_id()

        # Insert into the Doctor table
        query = "INSERT INTO Doctors (dr_id, dr_name, ph_no, Specialization, working_hrs, gender, age, salary, fees, username, park_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (dr_id, Doctor_Name, mobile_no, Specialisation, Working_Hrs, Gender, Age, Salary, Fees, username, park_id)
        cur.execute(query, values)
        db.commit()

        response = {
            'message': 'Doctor record inserted',
            'dr_id': dr_id
        }
        return jsonify(response), 201

    except Exception as error:
        return jsonify({'error': str(error)}), 500

    finally:
        # Close cursor and database connection if they were opened
        if cur:
            cur.close()
        if db:
            db.close()

def generate_park_id():
    return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + ''.join(random.choices('0123456789', k=3))

if __name__ == '__main__':
    app.run(debug=True)
