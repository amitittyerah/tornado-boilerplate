import logging
import logging.config

from datetime import datetime, timedelta

from models.user import UserToken
from Database.instance import Instance

log = logging.getLogger("root")


def token_authenticate():
    """
    This is a basic authentication interceptor which
    protects the desired URIs and requires
    authentication as per configuration
    """

    def wrapper(self, transforms, *args, **kwargs):
        def _request_basic_auth(self):
            if self._headers_written:
                raise Exception('headers have already been written')

            self.set_status(401)
            self.finish()
            return False

        request = self.request
        clazz = self.__class__
        log.debug('intercepting for class : %s', clazz)
        try:
            token = request.headers.get('token')
            if not token:
                return _request_basic_auth(self)

            session = Instance().get_session()
            user_token = session.query(UserToken)\
                .filter(UserToken.token == token)\
                .filter(UserToken.expires > datetime.utcnow())\
                .one()

            if user_token:
                self.token = user_token
                self.user = user_token.user

            else:
                return _request_basic_auth(self)
        except Exception, e:
            print e
            return _request_basic_auth(self)
        return True

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
                log.debug('Invoking wrapper %s', func)
                ret = func(self, transforms, *args, **kwargs)
                if ret:
                    return old(self, transforms, *args, **kwargs)
                else:
                    return ret

            return inner

        cls._execute = wrapper(cls._execute)
        return cls

    return classwrapper