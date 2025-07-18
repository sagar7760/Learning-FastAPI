from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db  # Fixed: was config.db
from models.models import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from services.user_services import UserService
from middlewares.auth import get_current_user
from typing import List

router = APIRouter()

class UserController:
    def __init__(self):
        self.user_service = UserService()

    @router.post("/register", response_model=Token, status_code=201)
    def register(self, user: UserCreate, db: Session = Depends(get_db)):
        """Register a new user"""
        return self.user_service.create_user(user, db)

    @router.post("/login", response_model=Token)
    def login(self, credentials: UserLogin, db: Session = Depends(get_db)):
        """User login"""
        return self.user_service.authenticate_user(credentials, db)

    @router.get("/", response_model=List[UserResponse])
    def get_users(self, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        """Get all users"""
        return self.user_service.get_all_users(db)

    @router.get("/{user_id}", response_model=UserResponse)
    def get_user(self, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        """Get user by ID"""
        return self.user_service.get_user_by_id(user_id, db)

    @router.put("/{user_id}", response_model=UserResponse)
    def update_user(self, user_id: int, user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        """Update user"""
        return self.user_service.update_user(user_id, user_data, db)

    @router.delete("/{user_id}")
    def delete_user(self, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        """Delete user"""
        return self.user_service.delete_user(user_id, db)

# Create controller instance
user_controller = UserController()