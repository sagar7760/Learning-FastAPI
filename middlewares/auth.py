from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
import os
from datetime import datetime
from config.database import get_db
from models.models import User

# Security scheme for bearer token
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"

class AuthMiddleware:
    """Authentication middleware class"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        JWT Token verification middleware
        
        Args:
            credentials: Bearer token from Authorization header
            
        Returns:
            str: Email extracted from token
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            # Decode JWT token
            payload = jwt.decode(
                credentials.credentials, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Extract email from token payload
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check token expiration
            exp = payload.get("exp")
            if exp is None or datetime.timezone.utc().timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return email
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_current_user(self, email: str = Depends(verify_token), db: Session = Depends(get_db)):
        """
        Get current authenticated user middleware
        
        Args:
            email: Email extracted from JWT token
            db: Database session
            
        Returns:
            User: Current authenticated user object
            
        Raises:
            HTTPException: If user not found or inactive
        """
        user = db.query(User).filter(User.email == email).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Check if user is active (if you have is_active field)
        if hasattr(user, 'is_active') and not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
        
        return user

    # def get_current_active_user(self, current_user: User = Depends(get_current_user)):
    #     """
    #     Get current active user (additional check for user status)
        
    #     Args:
    #         current_user: Current authenticated user
            
    #     Returns:
    #         User: Current active user object
            
    #     Raises:
    #         HTTPException: If user is inactive
    #     """
    #     if hasattr(current_user, 'is_active') and not current_user.is_active:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Inactive user"
    #         )
    #     return current_user

    # def admin_required(self, current_user: User = Depends(get_current_user)):
    #     """
    #     Admin authorization middleware
        
    #     Args:
    #         current_user: Current authenticated user
            
    #     Returns:
    #         User: Current admin user object
            
    #     Raises:
    #         HTTPException: If user is not admin
    #     """
    #     # Check if user has admin role
    #     if not getattr(current_user, 'is_admin', False):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Admin access required"
    #         )
    #     return current_user

    def optional_auth(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)), db: Session = Depends(get_db)):
        """
        Optional authentication middleware (for endpoints that work with or without auth)
        
        Args:
            credentials: Optional bearer token
            db: Database session
            
        Returns:
            User | None: Current user if authenticated, None otherwise
        """
        if credentials is None:
            return None
        
        try:
            email = self.verify_token(credentials)
            user = db.query(User).filter(User.email == email).first()
            return user
        except HTTPException:
            return None

# Create middleware instance
auth_middleware = AuthMiddleware()

# Export dependency functions for easy import
verify_token = auth_middleware.verify_token
get_current_user = auth_middleware.get_current_user
# admin_required = auth_middleware.admin_required
optional_auth = auth_middleware.optional_auth

# Role-based access decorators
# def require_roles(*roles):
#     """
#     Role-based access control decorator
    
#     Args:
#         *roles: Required roles for access
        
#     Returns:
#         Function: Dependency function that checks user roles
#     """
#     def role_checker(current_user: User = Depends(get_current_user)):
#         user_roles = getattr(current_user, 'roles', [])
#         if not any(role in user_roles for role in roles):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Access denied. Required roles: {', '.join(roles)}"
#             )
#         return current_user
    
#     return role_checker

# # Permission-based access control
# def require_permissions(*permissions):
#     """
#     Permission-based access control decorator
    
#     Args:
#         *permissions: Required permissions for access
        
#     Returns:
#         Function: Dependency function that checks user permissions
#     """
#     def permission_checker(current_user: User = Depends(get_current_user)):
#         user_permissions = getattr(current_user, 'permissions', [])
#         if not all(perm in user_permissions for perm in permissions):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Access denied. Required permissions: {', '.join(permissions)}"
#             )
#         return current_user
    
#     return permission_checker