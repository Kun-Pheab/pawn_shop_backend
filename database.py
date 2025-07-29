import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # This tries to load from .env if it's present IN THE CONTAINER

DATABASE_URL = os.getenv("DATABASE_URL")

# --- CRUCIAL DEBUGGING LINE ---
print(f"DEBUG: Value of DATABASE_URL before engine creation: '{DATABASE_URL}'")
# --- END CRITICAL DEBUGGING ---

# --- FALLBACK (ensure this is the EXACT URL that worked with psql) ---
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:Vg1%25%3B%7D%40g%3BN%7Ex%7EgU%3C@35.225.252.103:5432/postgres"
    print("⚠️ WARNING: DATABASE_URL not set in environment. Using fallback URL.")
# --- END FALLBACK ---

engine = create_engine( DATABASE_URL,
                        pool_size=50,
                        max_overflow=60,
                        pool_timeout=70,
                        pool_recycle=1800,
                        pool_pre_ping=True
                    )
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db # Assuming yield db for FastAPI dependency injection
    finally:
        db.close()