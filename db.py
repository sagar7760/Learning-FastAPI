from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql://root:Admin@123@localhost:3306/users"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session=sessionmaker(autoflush=False, autocommit=False, bind=engine)
base=declarative_base()

def get_db():
    db = session()
    try:
        yield db
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()