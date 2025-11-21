# Import the main SQLAlchemy components needed for database setup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy needs a database, a URL to locate it, an engine to manage connections, 
# and a session to perform operations

# Define the database URL. SQLite, "items.db" in the current directory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./items.db"

# Create the database engine. This is the interface that SQLAlchemy uses to communicate with the database.
# For SQLite, we add "check_same_thread=False" because FastAPI runs in multiple threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} #SQLite allows multiple threads to access the db
)

# Create a sessionmaker. This will be used to create database sessions for each request.
# autocommit=False: Don't automatically commit changes to the database.
# autoflush=False: Don't automatically flush changes to the database.
# bind=engine: Link this sessionmaker to our engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models. All model classes will inherit from this.
# It's needed for SQLAlchemy to map Python classes to database tables.
Base = declarative_base()
