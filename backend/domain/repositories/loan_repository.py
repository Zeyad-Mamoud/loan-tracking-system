from abc import ABC, abstractmethod
from typing import List
from domain.entities.loan import Loan

class LoanRepository(ABC):
    @abstractmethod
    def add(self, loan: Loan) -> Loan:
        pass

    @abstractmethod
    def get_by_id(self, loan_id: int) -> Loan:
        pass

    @abstractmethod
    def get_all(self) -> List[Loan]:
        pass

    @abstractmethod
    def update(self, loan: Loan) -> Loan:
        pass