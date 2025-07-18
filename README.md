## Learning FastAPI simple login page Using fastApi for backend adn React for Frontend

### TechStack used

- Backend: FastAPI
- Frontend: React, TailwindCSS
- Password Hashing: bcrypt (using passlib)

### Folder Structure of backend 
-        FastAPI/
        ├── config/
        │   └── db.py                 # Database configuration
        ├── models/
        │   └── models.py            # Database models
        ├── middlewares/
        │   └── auth.py              # Authentication middleware
        ├── routes/                  # or controllers/
        │   ├── __init__.py
        │   ├── auth.py              # Authentication routes
        │   └── users.py             # User CRUD routes
        ├── schemas/                 # Pydantic models
        │   └── user.py
        ├── services/                # Business logic
        │   └── user_service.py
        ├── utils/
        │   └── security.py          # Password hashing, JWT utils
        ├── .env
        ├── main.py
        └── requirements.txt
