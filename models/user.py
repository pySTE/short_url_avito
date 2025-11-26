from sqlalchemy import Column, Integer, String
from database.connection import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
