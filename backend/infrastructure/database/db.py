from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from domain.repositories.contact_repository import ContactRepository
from domain.entities.loan import Loan, LoanStatus, LoanType
from domain.entities.contact import Contact
from typing import List
from infrastructure.database.models import LoanModel, ContactModel, Base
from domain.repositories.loan_repository import LoanRepository
import os 
from fastapi import Depends
from datetime import date, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert postgres:// to postgresql:// if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

logger.info(f"Connecting to database with URL: {DATABASE_URL}")

# Create engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=5,         # Maximum number of connections to keep
    max_overflow=10      # Maximum number of connections that can be created beyond pool_size
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}")
    raise

class SQLAlchemyLoanRepository(LoanRepository):
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):
        if self._session is None:
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session

    def _handle_db_error(self, operation: str, e: Exception):
        logger.error(f"Database error during {operation}: {str(e)}")
        raise Exception(f"Database error during {operation}: {str(e)}")

    def get_upcoming_loans(self, days: int = 7) -> List[Loan]:
        try:
            today = date.today()
            end_date = today + timedelta(days=days)
            
            db_loans = self.session.query(LoanModel).filter(
                LoanModel.due_date >= today,
                LoanModel.due_date <= end_date,
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
        except Exception as e:
            self._handle_db_error("get_upcoming_loans", e)

    def add(self, loan: Loan) -> Loan:
        try:
            db_loan = LoanModel(**loan.__dict__)
            self.session.add(db_loan)
            self.session.commit()
            self.session.refresh(db_loan)
            return Loan(**db_loan.__dict__)
        except Exception as e:
            self.session.rollback()
            self._handle_db_error("add loan", e)

    def get_by_id(self, loan_id: int) -> Loan:
        try:
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
        except Exception as e:
            self._handle_db_error("get loan by id", e)

    def get_all(self) -> List[Loan]:
        try:
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
        except Exception as e:
            self._handle_db_error("get all loans", e)

    def update(self, loan: Loan) -> Loan:
        try:
            db_loan = self.session.query(LoanModel).filter(LoanModel.id == loan.id).first()
            for key, value in loan.__dict__.items():
                if key != "id" and value is not None:
                    setattr(db_loan, key, value)
            self.session.commit()
            self.session.refresh(db_loan)
            return Loan(**db_loan.__dict__)
        except Exception as e:
            self.session.rollback()
            self._handle_db_error("update loan", e)

    def get_contact_by_id(self, contact_id: int) -> Contact:
        try:
            db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
            return Contact(**db_contact.__dict__) if db_contact else None
        except Exception as e:
            self._handle_db_error("get contact by id", e)

class SQLAlchemyContactRepository(ContactRepository):
    def __init__(self, session: Session = None):
        self._session = session

    @property
    def session(self):
        if self._session is None:
            raise ValueError("Session is not provided. Use dependency injection.")
        return self._session

    def _handle_db_error(self, operation: str, e: Exception):
        logger.error(f"Database error during {operation}: {str(e)}")
        raise Exception(f"Database error during {operation}: {str(e)}")

    def add(self, contact: Contact) -> Contact:
        try:
            db_contact = ContactModel(**contact.__dict__)
            self.session.add(db_contact)
            self.session.commit()
            self.session.refresh(db_contact)
            return Contact(**db_contact.__dict__)
        except Exception as e:
            self.session.rollback()
            self._handle_db_error("add contact", e)

    def get_by_id(self, contact_id: int) -> Contact:
        try:
            db_contact = self.session.query(ContactModel).filter(ContactModel.id == contact_id).first()
            return Contact(**db_contact.__dict__) if db_contact else None
        except Exception as e:
            self._handle_db_error("get contact by id", e)

    def get_all(self) -> List[Contact]:
        try:
            db_contacts = self.session.query(ContactModel).all()
            return [Contact(**contact.__dict__) for contact in db_contacts]
        except Exception as e:
            self._handle_db_error("get all contacts", e)

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