from domain.repositories.loan_repository import LoanRepository

class ListLoansUseCase:
    def __init__(self, repository:LoanRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()