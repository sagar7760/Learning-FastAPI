from sqlalchemy import Column, Integer, String, DateTime

class User:
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True) 
    email= Column(String, unique=True, index=True)
    name=Column(String, index=True)
    password=Column(String, index=True)
    created_at=Column(DateTime, index=True)
    