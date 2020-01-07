
class User():
    def __init__(self, id, email, password, role_id):
        self.id = id
        self.email = email
        self.password = password
        self.role_id = role_id

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
