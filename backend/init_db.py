"""
Database initialization script.
Run this to create the database tables.
"""
from database import engine, Base
from models import Review

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()

