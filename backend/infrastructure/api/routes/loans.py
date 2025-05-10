from fastapi import APIRouter, Depends
from pydantic import BaseModel
from infrastructure.database.db import get_loan_repository
from domain.entities.loan import LoanType, Loan,LoanStatus
from application.use_cases.add_loan import AddLoanUseCase
from application.use_cases.list_loans import ListLoansUseCase
from datetime import datetime
from fastapi import HTTPException
from infrastructure.database.db import get_db
from sqlalchemy.orm import  Session
from typing import Optional, List
from application.use_cases.get_upcoming_loans import GetUpcomingLoansUseCase
from domain.entities.contact import Contact

router = APIRouter()

class LoanCreate(BaseModel):
    amount: float
    due_date: str  
    loan_type: LoanType
    contact_id: int

class LoanUpdate(BaseModel):
    status: Optional[str] = None
    payment_amount: Optional[float] = None

class UpcomingLoanResponse(BaseModel):
    id: int
    amount: float
    due_date: str
    loan_type: str
    contact_name: str
    remaining_balance: float

@router.post("/", response_model=Loan)
def create_loan(loan: LoanCreate, repo=Depends(get_loan_repository), db: Session = Depends(get_db)):
    try:
        due_date = datetime.strptime(loan.due_date, "%Y-%m-%d").date()
        print(f"Received loan data: {loan}")
        print(f"Parsed due_date: {due_date}")

        if not repo.get_contact_by_id(loan.contact_id):
            raise HTTPException(status_code=400, detail=f"Contact with ID {loan.contact_id} not found")

        use_case = AddLoanUseCase(repo)
        new_loan = use_case.execute(
            amount=loan.amount,
            due_date=due_date,
            loan_type=loan.loan_type.value,
            contact_id=loan.contact_id,
            status=LoanStatus.ACTIVE.value,  
            remaining_balance=loan.amount
        )
        
        return new_loan

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD. Error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.get("/", response_model=list[Loan])
def get_all_loans(repo=Depends(get_loan_repository), db: Session = Depends(get_db)):
    use_case = ListLoansUseCase(repo)
    return use_case.execute()

@router.patch("/{loan_id}", response_model=dict)
def update_loan(loan_id: int, loan: LoanUpdate, repo=Depends(get_loan_repository), db: Session = Depends(get_db)):
    try:
        loan_obj = repo.get_by_id(loan_id)
        if not loan_obj:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.status:
            valid_statuses = [status.value for status in LoanStatus]
            if loan.status not in valid_statuses:
                raise HTTPException(status_code=400, detail=f"Invalid status. Use one of: {', '.join(valid_statuses)}")
            if loan.status == LoanStatus.PARTIALLY_PAID.value and (loan.payment_amount is None or loan.payment_amount <= 0):
                raise HTTPException(status_code=400, detail="Payment amount must be provided and greater than 0 for partial payment.")

            # تحديث الـstatus والـremaining_balance
            if loan.status == LoanStatus.PARTIALLY_PAID.value:
                loan_obj.remaining_balance -= loan.payment_amount
                if loan_obj.remaining_balance < 0:
                    raise HTTPException(status_code=400, detail="Payment amount exceeds remaining balance.")
                loan_obj.status = LoanStatus.PARTIALLY_PAID.value if loan_obj.remaining_balance > 0 else LoanStatus.PAID.value
            else:
                loan_obj.status = loan.status
                if loan.status == LoanStatus.PAID.value:
                    loan_obj.remaining_balance = 0

        repo.update(loan_obj)
        return {"message": "Loan updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/upcoming", response_model=List[UpcomingLoanResponse])
def get_upcoming_loans(days: int = 7, repo=Depends(get_loan_repository), db: Session = Depends(get_db)):
    try:
        use_case = GetUpcomingLoansUseCase(repo)
        upcoming_loans = use_case.execute(days)
        
        # Get contact names for each loan
        response = []
        for loan in upcoming_loans:
            contact = repo.get_contact_by_id(loan.contact_id)
            if contact:
                response.append({
                    "id": loan.id,
                    "amount": loan.amount,
                    "due_date": loan.due_date.isoformat(),
                    "loan_type": loan.loan_type.value,
                    "contact_name": contact.name,
                    "remaining_balance": loan.remaining_balance
                    
                })
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))