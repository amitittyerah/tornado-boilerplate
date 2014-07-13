from sqlalchemy import create_engine
from sqlalchemy import Table, Column, DateTime, Integer, String, MetaData

metadata = MetaData()
engine = create_engine('sqlite:///dev.db', echo=True)

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String, unique=True),
                    Column('hashed_password', String),
                    Column('salt', String),
                    Column('created_on', DateTime))

user_tokens_table = Table('usertokens', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('user_id', String),
                          Column('token', String, unique=True),
                          Column('expires', DateTime))

metadata.create_all(engine)