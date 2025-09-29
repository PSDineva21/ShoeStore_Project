class User:


    def __init__(self, id, email, password, is_admin=False):
        self._id = id
        self._email = email
        self._password = password
        self._is_admin = is_admin

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def is_admin(self):
        return self._is_admin

    @email.setter
    def email(self, value):
        if "@" in value and "." in value:
            self._email = value
        else:
            raise ValueError("Невалиден имейл адрес")

    def check_password(self, password):
        return self._password == password

    def change_password(self, old_password, new_password):
        if self._password == old_password:
            self._password = new_password
            return True
        return False


class AuthService:

    def __init__(self):
        self._users = []
        self._next_id = 1
        self._initialize_admin()

    def _initialize_admin(self):
        self.register("admin@example.com", "admin123", True)

    @property
    def users_count(self):
        return len(self._users)

    def register(self, email, password, is_admin=False):
        if any(user.email == email for user in self._users):
            return None

        user = User(self._next_id, email, password, is_admin)
        self._next_id += 1
        self._users.append(user)
        return user

    def login(self, email, password):
        for user in self._users:
            if user.email == email and user.check_password(password):
                return user
        return None

    def get_user_by_id(self, user_id):
        for user in self._users:
            if user.id == user_id:
                return user
        return None


auth_service = AuthService()