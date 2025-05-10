from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from domain.repositories.contact_repository import ContactRepository
from domain.entities.loan import Loan, LoanStatus, LoanType
from domain.entities.contact import Contact
from typing import List
from infrastructure.database.models import LoanModel, ContactModel
from domain.repositories.loan_repository import LoanRepository
import os 
from fastapi import Depends
from datetime import date, timedelta
DATABASE_PUBLIC_URL = os.getenv("DATABASE_URL", "postgresql://cloudteam:Zikazika1%40@loantrackingpgsql.postgres.database.azure.com:5432/loan_db")
engine = create_engine(DATABASE_PUBLIC_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SQLAlchemyLoanRepository(LoanRepository):
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):  
        if self._session is None:
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session

    def to_dict(self, db_loan: LoanModel) -> dict:
        """
        Convert a LoanModel object to a dictionary.
        """
        return {
            'id': db_loan.id,
            'amount': db_loan.amount,
            'due_date': db_loan.due_date,
            'loan_type': db_loan.loan_type,
            'contact_id': db_loan.contact_id,
            'status': db_loan.status,
            'remaining_balance': db_loan.remaining_balance
        }

    def get_upcoming_loans(self, days: int = 7) -> List[Loan]:
        today = date.today()
        end_date = today + timedelta(days=days)
        
        db_loans = self.session.query(LoanModel).filter(
            LoanModel.due_date >= today,
            LoanModel.due_date <= end_date,
            LoanModel.status != LoanStatus.PAID.value
        ).all()
        
        return [Loan(**self.to_dict(loan)) for loan in db_loans]

    def add(self, loan: Loan) -> Loan:
        # Convert Loan entity to dict for database model
        loan_dict = {
            'amount': loan.amount,
            'due_date': loan.due_date,
            'loan_type': loan.loan_type,
            'contact_id': loan.contact_id,
            'status': loan.status,
            'remaining_balance': loan.remaining_balance
        }
        db_loan = LoanModel(**loan_dict)
        self.session.add(db_loan)
        self.session.commit()
        self.session.refresh(db_loan)
        return Loan(**self.to_dict(db_loan))

    def get_by_id(self, loan_id: int) -> Loan:
        db_loan = self.session.query(LoanModel).filter(LoanModel.id == loan_id).first()
        if not db_loan:
            return None
        return Loan(**self.to_dict(db_loan))

    def get_all(self) -> List[Loan]:
        db_loans = self.session.query(LoanModel).all()
        return [Loan(**self.to_dict(loan)) for loan in db_loans]

    def update(self, loan: Loan) -> Loan:
        db_loan = self.session.query(LoanModel).filter(LoanModel.id == loan.id).first()
        if not db_loan:
            return None
            
        # Update only the fields that are not None
        for key, value in loan.__dict__.items():
            if key != "id" and value is not None:
                setattr(db_loan, key, value)
                
        self.session.commit()
        self.session.refresh(db_loan)
        return Loan(**self.to_dict(db_loan))

    def get_contact_by_id(self, contact_id: int) -> Contact:
        db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
        if not db_contact:
            return None
        return Contact(
            id=db_contact.id,
            name=db_contact.name,
            email=db_contact.email,
            phone=db_contact.phone
        )

class SQLAlchemyContactRepository(ContactRepository):
    
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):
        if self._session is None:   
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session

    def to_dict(self, db_contact: ContactModel) -> dict:
        """
        Convert a ContactModel object to a dictionary.
        """
        return {
            "id": db_contact.id,
            "name": db_contact.name,
            "email": db_contact.email,
            "phone": db_contact.phone,
        }

    def add(self, contact: Contact) -> Contact:
        # Convert Contact entity to dict for database model
        contact_dict = {
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone
        }
        db_contact = ContactModel(**contact_dict)
        self.session.add(db_contact)
        self.session.commit()
        self.session.refresh(db_contact)
        return Contact(**self.to_dict(db_contact))

    def get_by_id(self, contact_id: int) -> Contact:
        db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
        return Contact(**self.to_dict(db_contact)) if db_contact else None

    def get_all(self) -> List[Contact]:
        db_contacts = self.session.query(ContactModel).all()
        return [Contact(**self.to_dict(contact)) for contact in db_contacts]

    def get_contact_by_id(self, contact_id: int) -> Contact:
        db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
        if not db_contact:
            return None
        return Contact(**self.to_dict(db_contact))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_loan_repository(session: Session = Depends(lambda: next(get_db()))):
    return SQLAlchemyLoanRepository(session)

def get_contact_repository(session: Session = Depends(lambda: next(get_db()))):
    return SQLAlchemyContactRepository(session)