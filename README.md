# Loan Tracking System

A full-stack web application for managing loans and contacts, built with FastAPI and React.

## Features

- Track loans with due dates and payment status
- Manage contacts with their loan history
- View upcoming loan payments
- Mark loans as paid or partially paid
- Real-time notifications for upcoming payments

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy
- APScheduler for notifications

### Frontend
- React
- CSS for styling
- Date-fns for date formatting

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
# Make sure PostgreSQL is running
# Update DATABASE_URL in .env if needed
```

5. Run the backend server:
```bash
uvicorn infrastructure.api.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `BACKEND_URL`: URL for the backend API

### Frontend
- `REACT_APP_BACKEND_URL`: URL for the backend API

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
