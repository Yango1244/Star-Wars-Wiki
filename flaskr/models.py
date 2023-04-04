from flask_login import UserMixin


class Users():

    def __init__(self):
        self.user_dict = {}

    def get_user(self, user_id):
        if user_id in self.user_dict:
            return self.user_dict[user_id]
        return None

    def add_user_from_id(self, user_id):
        self.user_dict[user_id] = User(user_id)


class User(UserMixin):

    def __init__(self, user_id):
        self.is_active_val = True
        self.is_authenticated_val = False
        self.is_anonymous_val = True
        self.user_id_val = user_id

    @property
    def user_id(self):
        return self.user_id_val

    @property
    def is_authenticated(self):
        return self.is_authenticated_val

    @property
    def is_active(self):
        return self.is_active_val

    @property
    def is_anonymous(self):
        return self.is_anonymous_val

    def get_id(self):
        return self.user_id_val

    @is_active.setter
    def is_active(self, value):
        self.is_active_val = value

    @is_authenticated.setter
    def is_authenticated(self, value):
        self.is_authenticated_val = value

    def authenticate(self):
        self.is_authenticated_val = True
        self.is_anonymous_val = False
