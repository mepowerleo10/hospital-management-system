# Mussa Mipawa
# Python 2.7

from flask_resful import Resource, Api, request
from package.model import conn
from package.user import User


class Admin(Resource, User):
    def __init__(self, id, first_name, last_name, email, password, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role_id = role_id

    def get(self, id):
        admin = conn.execute(
            "SELECT * FROM admin WHERE ad_id=?", (id,)).fetchall()
        return admin

    """ def delete(self, id):
        conn.execute() """

    def put(self, id):
        adminInput = request.get_json(force=True)
        ad_first_name = adminInput['ad_first_name']
        ad_last_name = adminInput['ad_last_name']
        ad_email = adminInput['ad_email']
        ad_password = adminInput['ad_password']
