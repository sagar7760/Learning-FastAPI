from sqlalchemy.orm import Session
from models.models import User
from schemas.user import UserCreate, UserLogin
from fastapi import HTTPException, status
from utils.secure import hash_password, verify_password, create_access_token
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./env_files/.env")

class UserService:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")

    def create_user(self, user_data: UserCreate, db: Session):
        """Create new user"""
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Use security utils
        hashed_password = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return self.generate_token_response(db_user)

    def authenticate_user(self, credentials: UserLogin, db: Session):
        """Authenticate user and return token"""
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user or not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return self.generate_token_response(user)

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_id(self, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, user_id: int, user_data: UserCreate, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.name = user_data.name
        user.email = user_data.email
        if user_data.password:
            user.password = hash_password(user_data.password)
        
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}

    def generate_token_response(self, user):
        """Generate JWT token response"""
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(hours=24)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400,  # 24 hours
            "user": user
        }