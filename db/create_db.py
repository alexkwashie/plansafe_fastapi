from .database import engine
from .models import Base

def create_tables():
    # Drop all existing tables
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables recreated successfully.")
