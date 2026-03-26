import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# We need to make sure the SQLite database file path is correct
# In Docker, it's mapped to /app/data/
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./triagem.db")

# For sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
