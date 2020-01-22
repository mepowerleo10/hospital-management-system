import enum


class Roles(enum.Enum):
    ADMIN = 0
    DOCTOR = 1
    PATIENT = 2

    def val(self):
        return self.value


SALT = "$2b$12$2P0MuLv7h7ARTUi78yXV2e"
