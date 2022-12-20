import re
from base.contrib.models import AbstractUser, BaseModelMixin
from config.db import db
from werkzeug.security import check_password_hash, generate_password_hash


class BaseUserModelMixin(AbstractUser, BaseModelMixin):
    REQURID_FIELDS = 'username', 'password', 'email'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    __email = None

    def __init__(self, **kwargs):
        for item, value in kwargs.items():
            estado = hasattr(self, item)
            if estado:
                setattr(self, item, value)

    @classmethod
    def get_required_fields(self):
        for item in self.REQURID_FIELDS:
            return item

    def __set_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if getattr(self, key):
                setattr(self, key, value)

    def validate_email(self, email=None):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if email:
            return re.match(expresion_regular, email) is not None
        else:
            return re.match(expresion_regular, self.email) is not None

    def set_password(self, password):
        new_password = generate_password_hash(password)
        return new_password

    def check_password(self, password):

        return check_password_hash(self.password, password)
