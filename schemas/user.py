from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: str = Field(..., description="User email address")
    name: str = Field(..., min_length=2, max_length=50, description="User full name")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=100, description="User password")
    
    @validator('email')
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        if not v or not v.strip():
            raise ValueError('Email is required')
        return v.lower().strip()
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name"""
        if not v or not v.strip():
            raise ValueError('Name is required')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password"""
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    @validator('email')
    def validate_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower().strip() if v else None

class UserResponse(BaseModel):
    """Schema for user responses (excludes sensitive data)"""
    id: int
    email: str
    name: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
