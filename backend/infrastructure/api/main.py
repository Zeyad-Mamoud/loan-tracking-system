from fastapi import FastAPI
from infrastructure.api.routes import loans, contacts
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from infrastructure.database.db import get_loan_repository, get_db
from application.use_cases.get_upcoming_loans import GetUpcomingLoansUseCase
from sqlalchemy.orm import Session
from fastapi import Depends
import logging
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(title="Loan Tracking System")

# Get CORS origins from environment variable
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(loans.router, prefix="/loans", tags=["loans"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to Loan Tracking System"}

# Create ASGI application
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)