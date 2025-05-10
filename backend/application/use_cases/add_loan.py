from domain.entities.loan import Loan
from datetime import date
from typing import Optional
from domain.repositories.loan_repository import LoanRepository

class AddLoanUseCase:
    def __init__(self, repository: LoanRepository):
        self.repository = repository

    def execute(
        self,
        amount: float,
        due_date: date,
        loan_type: str,
        contact_id: int,
        status: Optional[str] = None,
        remaining_balance: Optional[float] = None
    ) -> Loan:
        loan = Loan(
            id=None,
            amount=amount,
            due_date=due_date,
            loan_type=loan_type,
            contact_id=contact_id,
            status=status or "ACTIVE",  
            remaining_balance=remaining_balance or amount
        )
        return self.repository.add(loan)