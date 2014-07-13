from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Instance(object):
    def __init__(self):
        """
            Create a session
        """
        engine = create_engine('sqlite:///dev.db')
        self._session = sessionmaker(bind=engine)

    @classmethod
    def instance(cls):
        """Singleton like accessor to instantiate backend object"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_session(self):
        return self._session()