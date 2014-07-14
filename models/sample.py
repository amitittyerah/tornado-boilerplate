from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Attribute(Base):
    __tablename__ = 'attributes'

    _protected = ['id']

    id = Column(Integer, primary_key=True)
    attr_name = Column(String)
    attr_img = Column(String)

    def __init__(self):
        pass

    def as_dict(self):
        return {
            'id': self.id,
            'attr_name': self.attr_name,
            'attr_img': self.attr_img
        }

    def update(self, params):
        for param, value in params.iteritems():
            if hasattr(self, param) and param not in self._protected:
                setattr(self, param, value[0])
