from sqlalchemy import Column, Integer, String
from config.database import base

class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) 
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255), index=True)
    password = Column(String(255))
