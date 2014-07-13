from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from models.utils import Utils
from settings import settings

Base = declarative_base()

from datetime import datetime, timedelta
import hashlib


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    salt = Column(String)
    created_on = Column(DateTime, default=func.now())

    password = ''

    def __init__(self, username=None):
        self.username = username

    def _generate_salt(self):
        return hashlib.md5(str(datetime.now()) + ':' + self.username).hexdigest()

    def _generate_new_password(self):
        return hashlib.md5(self.salt + ' ' + self.password).hexdigest()

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.hashed_password
        }

    def check_password(self, password):
        self.password = password
        return self.hashed_password == self._generate_new_password()

    @staticmethod
    def register(params):
        user = User()
        user.username = params['username']
        user.password = params['password']
        user.salt = user._generate_salt()
        user.hashed_password = user._generate_new_password()

        return user


class UserToken(Base):
    __tablename__ = 'usertokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)
    expires = Column(DateTime)
    user = relationship(
        User,
        backref=backref('users',
                         uselist=True,
                         cascade='delete,all'))

    def as_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'expires': Utils.get_unix_timestamp(self.expires),
            'user': self.user.as_dict()
        }

    @staticmethod
    def _generate_token():
        return hashlib.md5(str(datetime.now()) +
                           "//" +
                           Utils.generate_random_string()).hexdigest()

    @staticmethod
    def generate_token_for_user(user):
        token = UserToken()
        token.user_id = user.id
        token.token = UserToken._generate_token()
        token.expires = datetime.now() + timedelta(days=settings['token_expiry'])
        return token