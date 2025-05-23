from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

# Create and save a new contact in the database
def create_contact(db: Session, contact: schemas.ContactCreate):
    existing= db.query(models.Contact).filter(models.Contact.phone == contact.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Contact already exists")
    db_contact = models.Contact(name=contact.name, phone=contact.phone, email=contact.email)
    db.add(db_contact)  # Add to the session
    db.commit()         # to save changes to database
    db.refresh(db_contact)  #to get the updated data
    return db_contact

# return all contacts from the database
def get_contacts(db: Session):
    return db.query(models.Contact).all()

# Search for contacts by name, phone, or email
def search_contact(db: Session, name: str = None, phone: str = None, email: str = None):
    query = db.query(models.Contact)

    # Filter by name, phone, or email 
    if name:
        query = query.filter(models.Contact.name.ilike(f"%{name}%"))
    if phone:
        query = query.filter(models.Contact.phone.ilike(f"%{phone}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))

    return query.all()

# Update an existing contact by serial no
def edit_contact(db: Session, sr:int, updated_contact: schemas.ContactCreate):
    # Find the contact by serial no
    contact = db.query(models.Contact).filter(models.Contact.sr == sr).first()
    if not contact:
        return None  # Return None if not found

    # Update only the provided fields
    if updated_contact.name is not None:
        contact.name = updated_contact.name
    if updated_contact.phone is not None:
        # Check if phone number is already exists
        existing = db.query(models.Contact).filter(models.Contact.phone == updated_contact.phone, models.Contact.sr != sr).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already exists")
        contact.phone = updated_contact.phone
    if updated_contact.email is not None:
        contact.email = updated_contact.email


    db.commit()         # Save changes
    db.refresh(contact) # Refresh the updated contact
    return contact

# Delete a contact by their serial number (sr)
def delete_contact(db: Session,sr):
    contact = db.query(models.Contact).filter(models.Contact.sr == sr).first()
    if not contact:
        return None  # Return None if not found
    db.delete(contact) 
    db.commit()         
    return contact
