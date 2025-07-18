from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv(dotenv_path="./env_files/.env")

# Load environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
# Create the database URL
ENCODED_PASSWORD = quote_plus(DB_PASSWORD)

# Now use it in your DATABASE_URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your environment variables.")     

engine = create_engine(DATABASE_URL)
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