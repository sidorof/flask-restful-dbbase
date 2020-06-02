# tests/models/user_address.py
import os
from datetime import date, datetime
from flask_restful_dbbase import DBBase, WriteOnlyColumn

os.environ['SQLALCHEMY_DATABASE_URI'] = ":memory:"

db = DBBase()


class User(db.Model):
    """
    This class creates a simplified user model. Note that no security measures on the password are taken, this package has no opinion on the security model used.
    However, the info parameter is used to mark the password as write-only.

    The username is used as an id to test proper url generation
    """
    __tablename__ = "user"

    # essential
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    password = db.WriteOnlyColumn(
        db.String(80), nullable=False, info={"write-only": True})
    email = db.Column(db.String(80), unique=True, nullable=False)

    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    company = db.Column(db.String(255), nullable=True)

    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    is_account_current = db.Column(db.Boolean, default=False, nullable=False)

    date_joined = db.Column(db.Date, default=date.today, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    addresses = db.relationship("Address", backref="user", lazy="immediate")

    SERIAL_STOPLIST = [
        'generate_password_hash',
        'valid_password',
    ]

    def __init__(
        self,
        username,
        password,
        email,
        first_name=None,
        last_name=None,
        company=None,
        is_superuser=False,
        is_staff=False,
        is_active=True,
        last_login=None,
    ):

        self.username = username
        # self.password = bcrypt.generate_password_hash(
        #    password, app.config.get('BCRYPT_LOG_ROUNDS')
        # ).decode()
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.is_superuser = is_superuser
        self.is_staff = is_staff
        self.is_active = is_active
        self.last_login = None

        self.date_joined = datetime.now()



class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("user.username"))

