from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User
from pydantic import BaseModel
from typing import List

router = APIRouter()


class userCraation(BaseModel):
    email:str
    name:str
    password:str

class userResponse(userCraation):
    id:int


router.get("/", response_model=List[userResponse])
def get_users(db: Session = Depends(get_db)):
    users=db.query(User).all()
    return users


router.post("/", response_model=userResponse)
def create_user(user: userCraation, db: Session = Depends(get_db)):
    db_user=user(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

router.put("/{email}", response_model=userResponse)
def upadate_user(email: str, user: userCraation, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

router.delete("/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}