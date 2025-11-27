from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, unique=True)
    email = Column(String, unique=True, default=None)
    new_url = Column(String)
    url = Column(String)