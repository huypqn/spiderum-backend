from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    identity_number = db.Column(db.String(32), index=True)
    phone_number = db.Column(db.String(32))

    def check_password(self, pw) -> object:
        return check_password_hash(self.password_hash, pw)

    def set_password(self, pw) -> None:
        self.password_hash = generate_password_hash(pw)
