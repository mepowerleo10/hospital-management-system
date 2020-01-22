from package.model import conn
from package.enums import SALT, Roles
import bcrypt


class User():
    def __init__(self, id,  email, password, role_id, conf_password):
        """ self.first_name = first_name
        self.last_name = last_name """
        self.id = id
        self.email = email
        self.password = password
        self.conf_password = conf_password
        self.role_id = role_id

    # def __init__(self):
    #     return None

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "role_id": self.role_id
        }

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    @staticmethod
    def check_user(email):
        user_t = conn.execute(
            "SELECT * FROM user WHERE email=?", (email,)).fetchone()
        # print user_t
        if user_t != None:
            user = User(user_t['id'], user_t['email'],
                        user_t['password'], user_t['role_id'], user_t['password'])
            return user
        else:
            return None

    @staticmethod
    def register(user):
        # salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), SALT)
        sql_admin = "INSERT INTO admin(ad_first_name, ad_last_name, ad_gender) VALUES(?,?,?)"
        uid = conn.execute(sql_admin, (user.first_name, user.last_name, 1,))
        print uid
        sql_user = "INSERT INTO user(id, email, password, role_id) VALUES(?,?,?,?)"
        uid = conn.execute(
            sql_user, (3, user.email, hashed_password, user.role_id,))

        conn.commit()


class NewAdmin():
    def __init__(self, first_name, last_name,  email, password, conf_password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.conf_password = conf_password

    @staticmethod
    def register(user):
        # salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'), SALT)
        sql_admin = "INSERT INTO admin(ad_first_name, ad_last_name) VALUES(?,?)"
        uid = conn.execute(sql_admin, (user.first_name,
                                       user.last_name)).lastrowid
        sql_user = "INSERT INTO user(id, email, password, role_id) VALUES(?,?,?,?)"
        uid = conn.execute(
            sql_user, (uid, user.email, hashed_password, Roles.ADMIN.val()))
        conn.commit()

        return True
