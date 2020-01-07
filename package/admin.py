# Mussa Mipawa
# Python 2.7

from flask_resful import Resource, Api, request
from package.model import conn


class Admin(Resource):
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
