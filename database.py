import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Check if the DATABASE_URL environment variable is set.
# This is how Render will provide the PostgreSQL connection string.
DATABASE_URL = os.getenv("DATABASE_URL")

# If the environment variable is not set, use the local SQLite database.
if DATABASE_URL is None:
    DATABASE_URL = "sqlite:///./library.db"
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False} # Needed for SQLite
    )
else:
    # If DATABASE_URL is set, connect to the PostgreSQL database.
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()