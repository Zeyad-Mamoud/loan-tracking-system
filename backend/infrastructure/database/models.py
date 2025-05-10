from sqlalchemy import Column, Integer, Float, Date, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import declarative_base
from domain.entities.loan import LoanType, LoanStatus

Base = declarative_base()

class LoanModel(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    loan_type = Column(SQLEnum(LoanType), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    status = Column(SQLEnum(LoanStatus), nullable=False)  
    remaining_balance = Column(Float, nullable=False)


class ContactModel(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)