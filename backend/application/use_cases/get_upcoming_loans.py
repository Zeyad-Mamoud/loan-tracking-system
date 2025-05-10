from domain.entities.loan import Loan
from typing import List
from domain.repositories.loan_repository import LoanRepository

class GetUpcomingLoansUseCase:
    def __init__(self, repository: LoanRepository):
        self.repository = repository

    def execute(self, days: int = 7) -> List[Loan]:
        return self.repository.get_upcoming_loans(days)