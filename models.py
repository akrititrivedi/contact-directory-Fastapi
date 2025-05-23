from sqlalchemy import Column, Integer, String
from database import Base

class Contact(Base):
    __tablename__ = "contacts"  # Name of the table in the database

    # Unique serial number, auto-incremented
    sr = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Contact's name (max length 100 characters, cannot be null)
    name = Column(String(100), nullable=False)

    # Contact's phone number (max length 15 characters, cannot be null)
    phone = Column(String(15), nullable=False)

    # Contact's email address (max length 100 characters, cannot be null)
    email = Column(String(100), nullable=False)
