from flask_restful import Resource, Api, request
from package.model import conn
from package.user import User


class LoginResource(Resource):
    def post(self):
        args = request.get_json()
        if 'email' in args and 'password' in args:
            user = User.login(args['password'])
            if user is None:
                return {'message': "Email or Password is wrong!"}, 404
            if user.password == args['password']:
                token = Token(user.rowid)
                conn.execute("INSERT INTO token(value, user_id) VALUES(?,?)")
                return {
                    "token": token.value
                }
            else:
                return {'message': "Email or Password is wrong!"}, 404
        else:
            return {
                "must include email and password!", 400
            }
