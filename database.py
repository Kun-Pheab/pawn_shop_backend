import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv() # This tries to load from .env if it's present IN THE CONTAINER

DATABASE_URL = os.getenv("DATABASE_URL")

# --- CRUCIAL DEBUGGING LINE ---
print(f"DEBUG: Value of DATABASE_URL before engine creation: '{DATABASE_URL}'")
# --- END CRITICAL DEBUGGING ---

def create_database_engine():
    """Create database engine with retry logic"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                DATABASE_URL,
                pool_size=50,
                max_overflow=60,
                pool_timeout=70,
                pool_recycle=1800,
                pool_pre_ping=True
            )
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"Database connection established successfully on attempt {attempt + 1}")
            return engine
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed on attempt {attempt + 1}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise e
        except Exception as e:
            print(f"Unexpected error during database connection: {e}")
            raise e

try:
    engine = create_database_engine()
except Exception as e:
    print(f"Error creating database engine: {e}")
    # Create a dummy engine for development/testing
    engine = None

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

def get_db():
    if not SessionLocal:
        raise Exception("Database not configured")
    db = SessionLocal()
    try:
        yield db # Assuming yield db for FastAPI dependency injection
    finally:
        db.close()