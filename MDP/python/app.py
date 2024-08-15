from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@mysql/doctors'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'somesecretkey'

db = SQLAlchemy()


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, location):
        self.email = email
        self.password = password
        self.location = location

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_email = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)

    def __init__(self, company_name, company_email, continent, region):
        self.company_name = company_name
        self.company_email = company_email
        self.continent = continent
        self.region = region

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name}, info={self.info})>"

    def __init__(self, name, info):
        self.name = name
        self.info = info

db.init_app(app)
with app.app_context():
    db.create_all()


# @app.route('/')
# def display_data():
#     doctors_data = Doctor.query.all()
#     submissions_data = Submission.query.all()

#     return render_template('displaydata.html', submissions=submissions_data, doctors=doctors_data)

@app.route('/', methods=['POST', 'GET'])
def patients():
    if request.method == 'POST':
        patient_name = request.form['patientName']
        patient_info = request.form['patientInfo']

        # add patient to database
        patient = Patient(name=patient_name, info=patient_info)
        #print(patient)
        db.session.add(patient)
        db.session.commit()

    patients_data = Patient.query.all()
    print(patients_data)
    return render_template('patients.html', patients=patients_data)

@app.route('/deletePatient', methods=['POST'])
def delete_patient():
    patient_name = request.form['patientName']
    patient_info = request.form['patientInfo']

    # delete patient from the database
    Patient.query.filter_by(name=patient_name, info=patient_info).delete()
    db.session.commit()

    return redirect(url_for('patients'))

@app.route('/updatePatient', methods=['POST'])
def update_patient():
    patient_name = request.form['patientName']
    patient_info = request.form['patientInfo']

    # update patient in the database
    Patient.query.filter_by(name=patient_name).update({'info': patient_info})
    db.session.commit()

    return redirect(url_for('patients'))

print("Script is being executed")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Print a message to indicate that tables have been created
    print("Tables created successfully")

    app.run(debug=True, host='0.0.0.0')

