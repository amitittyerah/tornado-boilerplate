import logging
import logging.config

from datetime import datetime

from models.user import UserToken
from database.instance import Instance

log = logging.getLogger("auth")


def get_user(token):
    session = Instance().get_session()
    return session.query(UserToken) \
        .filter(UserToken.token == token) \
        .filter(UserToken.expires > datetime.utcnow()) \
        .one()


def token_authenticate():
    """
    This is a basic authentication interceptor which
    protects the desired URIs and requires
    authentication as per configuration
    """

    def wrapper(self, transforms, *args, **kwargs):

        request = self.request
        try:
            token = request.arguments.get('token')[0]
            if not token:
                return False

            user_token = get_user(token)

            if user_token:
                self.token = user_token
                self.user = user_token.user
                return True
        except:
            pass
        return False

    return wrapper


def interceptor(func):
    """
    This is a class decorator which is helpful in configuring
    one or more interceptors which are able to intercept, inspect,
    process and approve or reject further processing of the request
    """

    def classwrapper(cls):
        def wrapper(old):
            def inner(self, transforms, *args, **kwargs):
                ret = func(self, transforms, *args, **kwargs)
                if ret:
                    return old(self, transforms, *args, **kwargs)
                else:
                    self._transforms = transforms
                    return self._unauthorized()

            return inner

        cls._execute = wrapper(cls._execute)
        return cls

    return classwrapper