from core.utils.firebase_utils import change_password
from user.models import User

DEACTIVATION_PREFIX = 'deactivated_'


class Auth:
    def __init__(self, user):
        if not user or not isinstance(user, User):
            raise Exception("Valid User is required")
        self.user = user

    def change_password(self, password):
        self.user.set_password(password)
        self.user.save()
        if self.user.fid:
            change_password(self.user.fid, password)

    def deactivate(self):
        self.user.is_active = False
        self.user.save()
