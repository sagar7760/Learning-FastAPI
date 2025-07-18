from fastapi import FastAPI
from config.database import engine, base
from controllers.user_controller import router as user_router

app = FastAPI(
    title="User Management API",
    description="FastAPI application for user authentication and management",
    version="1.0.0"
)

# Create database tables
base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router, prefix="/users", tags=["User Management"])

@app.get("/")
def root():
    return {
        "message": "User Management API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}



