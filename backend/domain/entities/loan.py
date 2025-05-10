from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

class LoanType(Enum):
    BORROWED = "BORROWED"
    LENT = "LENT"

class LoanStatus(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"

@dataclass
class Loan:
    id: Optional[int]
    amount: float
    due_date: date
    loan_type: LoanType
    contact_id: int
    status: LoanStatus
    remaining_balance: float