# Ferdinand Kamuzora
# Python 2.7

from flask_restful import Resource, Api, request
from flask import render_template, session
from package.model import conn
from package.enums import SALT, Roles
import bcrypt


class Doctors(Resource):
    """This contain apis to carry out activity with all doctors"""

    def get(self):
        """Retrive list of all the doctor"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                doctors = conn.execute(
                    "SELECT * FROM doctor ORDER BY doc_date DESC").fetchall()
                return doctors
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
        """Add the new doctor"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                doctorInput = request.get_json(force=True)
                doc_first_name = doctorInput['doc_first_name']
                doc_last_name = doctorInput['doc_last_name']
                doc_ph_no = doctorInput['doc_ph_no']
                doc_address = doctorInput['doc_address']
                doc_password = doctorInput['doc_password']
                doc_email = doctorInput['doc_email']
                doctorInput['doc_id'] = conn.execute('''INSERT INTO doctor(doc_first_name,doc_last_name,doc_ph_no,doc_address)
                    VALUES(?,?,?,?)''', (doc_first_name, doc_last_name, doc_ph_no, doc_address)).lastrowid
                hashed_password = bcrypt.hashpw(
                    doc_password.encode('utf-8'), SALT)
                doc_id = doctorInput['doc_id']
                r = conn.execute(
                    "INSERT INTO user(id, email, password, role_id) VALUES(?,?,?,?)", (doc_id, doc_email, hashed_password, Roles.DOCTOR.val()))
                conn.commit()
                return doctorInput
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


class Doctor(Resource):
    """It include all the apis carrying out the activity with the single doctor"""

    def get(self, id):
        """get the details of the docktor by the doctor id"""

        try:
            if session['role_id'] == Roles.ADMIN.val():
                doctor = conn.execute(
                    "SELECT * FROM doctor WHERE doc_id=?", (id,)).fetchall()
                return doctor
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
        """Delete the doctor by its id"""

        try:
            if session['role_id'] == Roles.ADMIN.val():
                conn.execute("DELETE FROM doctor WHERE doc_id=?", (id,))
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
        """Update the doctor by its id"""
        try:
            if session['role_id'] == Roles.ADMIN.val():
                doctorInput = request.get_json(force=True)
                doc_first_name = doctorInput['doc_first_name']
                doc_last_name = doctorInput['doc_last_name']
                doc_ph_no = doctorInput['doc_ph_no']
                doc_address = doctorInput['doc_address']
                conn.execute(
                    "UPDATE doctor SET doc_first_name=?,doc_last_name=?,doc_ph_no=?,doc_address=? WHERE doc_id=?",
                    (doc_first_name, doc_last_name, doc_ph_no, doc_address, id))
                conn.commit()
                return doctorInput
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
        return render_template("/doctor-home.html")
