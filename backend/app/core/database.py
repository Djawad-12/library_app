from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from dotenv import load_dotenv
import os

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


