from pydantic import BaseModel, validator,Field
from typing import Optional
import re

# BaseModel defines common fields shared by both input and output
class ContactBase(BaseModel):
    name: Optional[str] = Field(
        default=None, example="Example Name", description="write your name")  # Person's name
    phone: Optional[str] = Field(
        default=None, example="+910000000000",description= "write 10 digit phone number")  # Phone number 
    email: Optional[str] = Field(
        default=None, example="Example@domain.com",description="write a valid email")  # Email
    
    @validator('name') # Validator to make sure  the name contains only letters and spaces
    def validate_name(cls,value):
        if value is None:
            return value
        name_pattern = r'^[A-za-z ]+$'
        if not re.match(name_pattern,value):
            raise ValueError("Name must contain only spaces and letters")
        return value 

    @validator('email')  # Validator to make sure  the email format is valid
    def validate_email(cls, value):
        if value is None:
            return value
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError("Email format is invalid")
        return value

    @validator('phone')  # Validator to make sure  the phone have valid country code and is 10 digit long
    def validate_phone(cls, value):
        if value is None:
            return value
        
        value = value.replace(" ", "")

        if not value.startswith("+"):
            raise ValueError("Please enter a valid country code with '+' (e.g., +91)")

        phone_pattern = r"^\+\d{1,2}\s?\d{10}$" 
        if not re.match(phone_pattern, value):
            raise ValueError("Phone number must have a valid country code and 10 digit long")
        return value

# Used when creating a new contact
class ContactCreate(ContactBase):
    pass

# Used for sending contact data as response
class ContactResponse(ContactBase):
    sr: int  # Serial number

    class Config:  # enables orm mode
        from_attributes = True
