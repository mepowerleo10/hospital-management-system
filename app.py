# Ferdinand Kamuzora
# Python 2.7

from flask import Flask, send_from_directory, render_template, session, flash, redirect, request, abort
from flask_restful import Resource, Api
from package.patient import Patients, Patient
from package.doctor import Doctors, Doctor
from package.appointment import Appointments, Appointment
from package.common import Common
from package.login import LoginResource
from package.user import User
from package.model import conn
import json

from flask_login import login_required, login_manager


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
# api.add_resource(LoginResource, '/login')

# Routes


@app.route('/')
def index():
    return app.send_static_file('index.html')


""" @app.route('/patient')
def patient():
    if not session.get('logged_in'):
        return render_template('patient.html')
    else:
        return redirect('/') """


def database(email):
    user_t = conn.execute(
        "SELECT * FROM user WHERE email=?", (email,)).fetchone()
    user = User(user_t['id'], user_t['email'],
                user_t['password'], user_t['role_id'])
    return user
    # print user_t


@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    user = database(email)
    if user.password == password:
        return redirect('patient.html')


@app.route("/login", methods=["GET"])
def get_login():
    return app.send_static_file('login.html')


if __name__ == '__main__':
    app.run(debug=True, host=config['host'], port=config['port'])
