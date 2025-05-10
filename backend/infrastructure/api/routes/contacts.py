from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from infrastructure.database.db import get_contact_repository, get_db
from domain.entities.contact import Contact
from typing import Optional, List
from sqlalchemy.orm import Session
from application.use_cases.list_contacts import ListContactsUseCase

router = APIRouter()

class ContactCreate(BaseModel):
    name: str
    phone: Optional[str]
    email: Optional[str]

@router.get("/", response_model=List[Contact])
def get_all_contacts(repo=Depends(get_contact_repository), db: Session = Depends(get_db)):
    try:
        use_case = ListContactsUseCase(repo)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch contacts: {str(e)}")

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, repo=Depends(get_contact_repository)):
    try:
        contact_entity = Contact(id=None, name=contact.name, phone=contact.phone, email=contact.email)
        return repo.add(contact_entity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create contact: {str(e)}")