FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including main.py)
COPY . .

# Run uvicorn using root-level main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]