from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas
from typing import Optional

app = FastAPI( title="Contact Directory",
    description="Manage your contact list.",)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to add a new contact
@app.post("/contacts/", response_model=schemas.ContactResponse,description="""
Add contact by giving name,phone and email.
          It will return error if phone number already exists.""")
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

# Route to search for contacts by name, phone, or email or show all contacs
@app.get("/contacts/", response_model=list[schemas.ContactResponse],description="""
Get all contacts or search by name, phone, or email.""" )
def search_contact(
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not any([name,phone,email]):
        return crud.get_contacts(db)
    
    
    contact = crud.search_contact(db, name=name, phone=phone, email=email)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Route to update contact by serial no
@app.put("/contacts/{sr}", response_model=schemas.ContactResponse,description="""
Edit contact by serial no.""")
def edit_contact(sr:int, updated_contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    contact = crud.edit_contact(db, sr, updated_contact)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Route to delete contact by serial no
@app.delete("/contacts/{sr}",description="""
Delete contact by serial no.""")
def delete_contact(sr, db: Session = Depends(get_db)):
    contact = crud.delete_contact(db, sr)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}
