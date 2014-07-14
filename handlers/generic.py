from sqlalchemy.orm.exc import NoResultFound

from handlers.base import BaseHandler
from handlers.auth import *
from models.sample import *
from models.response import Response

import sys
import logging
import inspect

@interceptor(token_authenticate())
class GenericHandler(BaseHandler):
    def get(self, cls, slug=None):
        session = self.backend.get_session()
        response = Response()
        cls_obj = getattr(sys.modules[__name__], cls)
        if inspect.isclass(cls_obj):
            try:
                objs = session.query(cls_obj)
                if slug:
                    obj = objs.filter(cls_obj.id == slug).one()
                    response.add_data(obj.as_dict())
                else:
                    response.add_data([obj.as_dict() for obj in objs])
            except NoResultFound:
                response.add_error_message('No such %s' % cls)
            except:
                response.add_error_message('Exception while fetching %s' % cls)
        else:
            response.add_error_message('No such class %s' % cls)
        self.write(response.as_dict())

    def post(self, cls, slug=None):
        session = self.backend.get_session()
        response = Response()
        cls_obj = getattr(sys.modules[__name__], cls)
        if inspect.isclass(cls_obj):
            try:
                obj = cls_obj()
                obj.update(self.request.arguments)
                session.add(obj)
                session.commit()
                response.add_data(obj.as_dict())
            except:
                session.rollback()
                response.add_error_message('Exception while fetching cards')
        else:
            response.add_error_message('No such class %s' % cls)
        self.write(response.as_dict())

    def delete(self, cls, slug=None):
        session = self.backend.get_session()
        response = Response()
        cls_obj = getattr(sys.modules[__name__], cls)
        if inspect.isclass(cls_obj):
            try:
                if slug:
                    session.query(cls_obj).filter(cls_obj.id == slug).delete()
                    session.commit()
                    response.add_data('Deleted')
                else:
                    response.add_error_message('Missing %s id' % cls)
            except:
                response.add_error_message('Exception while fetching cards')
        else:
            response.add_error_message('No such class %s' % cls)
        self.write(response.as_dict())

    def put(self, cls, slug=None):
        session = self.backend.get_session()
        response = Response()
        cls_obj = getattr(sys.modules[__name__], cls)
        if inspect.isclass(cls_obj):
            try:
                if slug:
                    obj = session.query(cls_obj).filter(cls_obj.id == slug).one()
                    obj.update(self.request.arguments)
                    session.add(obj)
                    session.commit()
                    response.add_data(obj.as_dict())
                else:
                    response.add_error_message('Missing %s id' % cls)
            except NoResultFound:
                response.add_error_message('Missing %s' % cls)
            except:
                response.add_error_message('Exception while fetching %s' % cls)
            finally:
                session.rollback()
        else:
            response.add_error_message('No such class %s' % cls)
        self.write(response.as_dict())

