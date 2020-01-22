# Ferdinand Kamuzora
# Python 2.7

from flask_restful import Resource, Api, request
from flask import session, render_template
from package.model import conn
# from app import app
from package.enums import Roles, SALT
import bcrypt


class Patients(Resource):
    """It contain all the api carryign the activity with aand specific patient"""

    def get(self):
        """Api to retive all the patient from the database"""
        try:
            if 1 == 1:
                patients = conn.execute(
                    "SELECT * FROM patient  ORDER BY pat_date DESC").fetchall()
                return patients
            else:
                return {
                    'status': 401,
                    'msg': 'Not authorized'
                }
        except KeyError as no_key:
            return {
                'status': 403,
                'msg': 'Forbidden'
            }

    def post(self):
        """api to add the patient in the database"""

        try:
            if session['role_id'] == Roles.ADMIN.val():
                patientInput = request.get_json(force=True)
                pat_first_name = patientInput['pat_first_name']
                pat_last_name = patientInput['pat_last_name']
                pat_insurance_no = patientInput['pat_insurance_no']
                pat_ph_no = patientInput['pat_ph_no']
                pat_address = patientInput['pat_address']
                pat_email = patientInput['pat_email']
                pat_password = patientInput['pat_password']
                patientInput['pat_id'] = conn.execute('''INSERT INTO patient(pat_first_name,pat_last_name,pat_insurance_no,pat_ph_no,pat_address)
                    VALUES(?,?,?,?,?)''', (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address)).lastrowid
                hashed_password = bcrypt.hashpw(
                    pat_password.encode('utf-8'), SALT)
                pat_id = patientInput['pat_id']
                r = conn.execute(
                    "INSERT INTO user(id, email, password, role_id) VALUES(?,?,?,?)", (pat_id, pat_email, hashed_password, Roles.PATIENT.val()))
                conn.commit()
                return patientInput
            else:
                return {
                    'status': 401,
                    'msg': 'Not authorized'
                }
        except KeyError as no_key:
            return {
                'status': 403,
                'msg': 'Forbidden'
            }


class Patient(Resource):
    """It contains all apis doing activity with the single patient entity"""

    def get(self, id):
        """api to retrive details of the patient by it id"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                patient = conn.execute(
                    "SELECT * FROM patient WHERE pat_id=?", (id,)).fetchall()
                return patient
            else:
                return {
                    'status': 401,
                    'msg': 'Not authorized'
                }
        except KeyError as no_key:
            return {
                'status': 403,
                'msg': 'Forbidden'
            }

    def delete(self, id):
        """api to delete the patiend by its id"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                conn.execute("DELETE FROM patient WHERE pat_id=?", (id,))
                conn.commit()
                return {'msg': 'sucessfully deleted'}
            else:
                return {
                    'status': 401,
                    'msg': 'Not authorized'
                }
        except KeyError as no_key:
            return {
                'status': 403,
                'msg': 'Forbidden'
            }

    def put(self, id):
        """api to update the patient by it id"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                patientInput = request.get_json(force=True)
                pat_first_name = patientInput['pat_first_name']
                pat_last_name = patientInput['pat_last_name']
                pat_insurance_no = patientInput['pat_insurance_no']
                pat_ph_no = patientInput['pat_ph_no']
                pat_address = patientInput['pat_address']
                conn.execute("UPDATE patient SET pat_first_name=?,pat_last_name=?,pat_insurance_no=?,pat_ph_no=?,pat_address=? WHERE pat_id=?",
                             (pat_first_name, pat_last_name, pat_insurance_no, pat_ph_no, pat_address, id))
                conn.commit()
                return patientInput
            else:
                return {
                    'status': 401,
                    'msg': 'Not authorized'
                }
        except KeyError as no_key:
            return {
                'status': 403,
                'msg': 'Forbidden'
            }

    @staticmethod
    def home():
        return render_template("/patient-home.html")
