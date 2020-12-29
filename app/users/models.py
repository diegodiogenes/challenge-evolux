from passlib.hash import pbkdf2_sha256
from app.utils import db
from passlib.hash import pbkdf2_sha256


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, username, password):
        """
        Implements the constructor to set password properly
        """
        self.username = username
        self.generate_password(password)

    def generate_password(self, password):
        """
        Takes the password and make the properly hash operation before set it
        """
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password) -> bool:
        """
        Takes the password and verify if the password matches with the user password
        """
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    def get_by_login(cls, username: str, password: str):
        user = User.get_by_username(username=username)
        if user.verify_password(password):
            return user
        return None

    @classmethod
    def get_by_username(cls, username: str):
        return User.query.filter_by(username=username).first()