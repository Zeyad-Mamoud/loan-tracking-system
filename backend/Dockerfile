FROM python:3.9-slim

WORKDIR /app

# Update pip
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install apscheduler


# Verify uvicorn is installed
RUN pip show uvicorn

# Copy the rest of the application
COPY . .

# Run uvicorn
CMD ["uvicorn", "infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]