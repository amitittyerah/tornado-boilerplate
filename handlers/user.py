from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from handlers.base import BaseHandler
from handlers.auth import *

from models.user import User, UserToken
from models.response import Response

import logging

logger = logging.getLogger('boilerplate.' + __name__)


class RegisterHandler(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        response = Response()
        try:
            username = self.get_argument('username', None, True)
            password = self.get_argument('password', None, True)
            user = User.register({'username': username, 'password': password})
            session.add(user)
            session.commit()
            response.add_data(user.as_dict())
        except IntegrityError:
            response.add_error_message('Username already exists')
        except Exception:
            response.add_error_message('Exception while adding a new user')
        finally:
            session.rollback()
        self.write(response.as_dict())


class LoginHandler(BaseHandler):
    def get(self):
        session = self.backend.get_session()
        response = Response()
        try:
            username = self.get_argument('username', None, True)
            password = self.get_argument('password', None, True)
            user = session.query(User).filter(User.username == username).one()
            if user.check_password(password):
                session.query(UserToken).filter(UserToken.user_id == user.id).delete()
                token = UserToken.generate_token_for_user(user)
                session.add(token)
                session.commit()
                response.add_data(token.as_dict())
            else:
                raise NoResultFound
        except NoResultFound:
            response.add_error_message('User does not exist')
        except IntegrityError:
            response.add_error_message('Token already exists. Retry')
        except Exception:
            response.add_error_message('Exception while generating a token')
        finally:
            session.rollback()
        self.write(response.as_dict())

@interceptor(token_authenticate())
class TestAuthHandler(BaseHandler):
    def get(self):
        self.write({'response': 200})