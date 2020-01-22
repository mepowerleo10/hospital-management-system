# Ferdinand Kamuzora
# Python 2.7

from flask import Flask, send_from_directory, render_template, session, flash, redirect, request, abort
from flask_restful import Resource, Api
from package.patient import Patients, Patient
from package.doctor import Doctors, Doctor
from package.appointment import Appointments, Appointment, PatientAppointments, DoctorAppointments
from package.common import Common
from package.login import LoginResource
from package.user import User
from package.model import conn
from package.enums import *
from package.register import Register
import bcrypt
import json
import os


with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
api = Api(app)

api.add_resource(Patients, '/patient')
api.add_resource(Patient, '/patient/<int:id>')
api.add_resource(Doctors, '/doctor')
api.add_resource(Doctor, '/doctor/<int:id>')
api.add_resource(Appointments, '/appointment')
api.add_resource(Appointment, '/appointment/<int:id>')
api.add_resource(Common, '/common')
api.add_resource(PatientAppointments, '/patient-appointments')
api.add_resource(DoctorAppointments, '/doctor-appointments')

# api.add_resource(LoginResource, '/login')


def check_access(url):
    try:
        role_id = session['role_id']
        logged_in = session['logged_in']
        if logged_in and role_id == Roles.ADMIN.val():
            return True
    except KeyError as ke:
        return False

# Routes
@app.route('/')
def home():
    try:
        role_id = session['role_id']
        if role_id == Roles.ADMIN.val():
            return redirect('/admin-dashboard')
        elif role_id == Roles.DOCTOR.val():
            return redirect('/doctor-home')
        elif role_id == Roles.PATIENT.val():
            return redirect('/patient-home')
        else:
            return redirect('/login')
    except expression as identifier:
        return redirect('/login')


@app.route('/patient.html')
def patients_page():
    # print session
    try:
        role_id = session['role_id']
        logged_in = session['logged_in']
        if logged_in and role_id == Roles.ADMIN.val():
            return render_template('patient.html')
    except KeyError as ke:
        print "Key: " + ke.message + " was not found!"
        if check_access('/patient/html'):
            return render_template('patient.html')
        else:
            return redirect('/login')


@app.route('/doctor.html')
def doctors_page():
    # print session
    try:
        role_id = session['role_id']
        logged_in = session['logged_in']
        if logged_in and role_id == Roles.ADMIN.val():
            return render_template('doctor.html')
    except KeyError as ke:
        print "Key: " + ke.message + " was not found!"
        if check_access('/doctor.html'):
            return render_template('doctor.html')
        else:
            return redirect('/login')


@app.route('/admin-dashboard')
def index():
    try:
        role_id = session['role_id']
        logged_in = session['logged_in']
        if logged_in and role_id == Roles.ADMIN.val():
            return render_template('admin.html')
    except KeyError as ke:
        print "Key: " + ke.message + " was not found!"
        # print session
        flash("Please login first!")
        return redirect('/login')


@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password'].encode('utf-8')
    user = User.check_user(email)
    if user == None:
        flash('Wrong email or password')
        return get_login()
    if user.password == bcrypt.hashpw(password, SALT):
        session['logged_in'] = True
        session['role_id'] = user.role_id
        if user.role_id == Roles.ADMIN.val():
            session['id'] = user.get_id()
            return redirect('/admin-dashboard')
        elif user.role_id == Roles.DOCTOR.val():
            session['doc_id'] = user.get_id()
            return redirect('/doctor-home.html')
        else:
            session['pat_id'] = user.get_id()
            return redirect('/patient-home.html')

    else:
        flash('Wrong email or password')
        return get_login()


@app.route("/login", methods=["GET"])
def get_login():
    return render_template('login.html')


@app.route("/register", methods=["GET"])
def get_registration():
    return Register.get()


@app.route("/register", methods=["POST"])
def post_registration():
    return Register.post()


@app.route("/patient-home", methods=["GET"])
def patient_home():
    return Patient.home()


@app.route("/doctor-home", methods=["GET"])
def doctor_home():
    return Doctor.home()


@app.route("/appointment.html", methods=["GET"])
def get_appointments():
    return Appointment.get_appointments()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host=config['host'], port=config['port'])
