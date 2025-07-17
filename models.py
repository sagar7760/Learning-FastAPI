from sqlalchemy import Column, Integer, String
from  db import base


class User(base):
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True) 
    email= Column(String, unique=True, index=True)
    name=Column(String, index=True)
    password=Column(String, index=True)
    