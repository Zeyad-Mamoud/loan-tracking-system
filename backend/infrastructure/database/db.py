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

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:11020044@db:5432/loan_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SQLAlchemyLoanRepository(LoanRepository):
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):
        if self._session is None:
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session
    def get_upcoming_loans(self, days: int = 7) -> List[Loan]:
        today = date.today()
        end_date = today + timedelta(days=days)
        
        db_loans = self.session.query(LoanModel).filter(
            LoanModel.due_date >= today.date(),
            LoanModel.due_date <= end_date.date(),
            LoanModel.status != LoanStatus.PAID.value
        ).all()
        
        loans = []
        for db_loan in db_loans:
            loan_dict = {
                'id': db_loan.id,
                'amount': db_loan.amount,
                'due_date': db_loan.due_date,
                'loan_type': db_loan.loan_type,
                'contact_id': db_loan.contact_id,
                'status': db_loan.status,
                'remaining_balance': db_loan.remaining_balance
            }
            loans.append(Loan(**loan_dict))
        
        return loans

    def add(self, loan: Loan) -> Loan:
        db_loan = LoanModel(**loan.__dict__)
        self.session.add(db_loan)
        self.session.commit()
        self.session.refresh(db_loan)
        return Loan(**db_loan.__dict__)

    def get_by_id(self, loan_id: int) -> Loan:
        db_loan = self.session.query(LoanModel).filter(LoanModel.id == loan_id).first()
        if not db_loan:
            return None
            
        loan_dict = {
            'id': db_loan.id,
            'amount': db_loan.amount,
            'due_date': db_loan.due_date,
            'loan_type': db_loan.loan_type,
            'contact_id': db_loan.contact_id,
            'status': db_loan.status,
            'remaining_balance': db_loan.remaining_balance
        }
        return Loan(**loan_dict)

    def get_all(self) -> List[Loan]:
        db_loans = self.session.query(LoanModel).all()
        loans = []
        for db_loan in db_loans:
            loan_dict = {
                'id': db_loan.id,
                'amount': db_loan.amount,
                'due_date': db_loan.due_date,
                'loan_type': db_loan.loan_type,
                'contact_id': db_loan.contact_id,
                'status': db_loan.status,
                'remaining_balance': db_loan.remaining_balance
            }
            loans.append(Loan(**loan_dict))
        return loans

    def update(self, loan: Loan) -> Loan:
        db_loan = self.session.query(LoanModel).filter(LoanModel.id == loan.id).first()
        for key, value in loan.__dict__.items():
            if key != "id" and value is not None:
                setattr(db_loan, key, value)
        self.session.commit()
        self.session.refresh(db_loan)
        return Loan(**db_loan.__dict__)

    def get_contact_by_id(self, contact_id: int) -> Contact:
        db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
        return Contact(**db_contact.__dict__) if db_contact else None

class SQLAlchemyContactRepository(ContactRepository):
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):
        if self._session is None:
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session

    def add(self, contact: Contact) -> Contact:
        with self.session as session:
            db_contact = ContactModel(**contact.__dict__)
            session.add(db_contact)
            session.commit()
            session.refresh(db_contact)
            return Contact(**db_contact.__dict__)

    def get_by_id(self, contact_id: int) -> Contact:
        with self.session as session:
            db_contact = session.query(ContactModel).filter(ContactModel.id == contact_id).first()
            return Contact(**db_contact.__dict__) if db_contact else None

    def get_all(self) -> List[Contact]:
        with self.session as session:
            db_contacts = session.query(ContactModel).all()
            return [Contact(**contact.__dict__) for contact in db_contacts]

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