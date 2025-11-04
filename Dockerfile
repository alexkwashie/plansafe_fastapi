FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Use the Railway-provided PORT environment variable
ENV PORT=8000

# Set environment variables
ENV SUPABASE_URL=https://eclxbmhyxwoxzwdcjaft.supabase.co
ENV SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjbHhibWh5eHdveHp3ZGNqYWZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3MjkyNDcsImV4cCI6MjA2ODMwNTI0N30.4xumTgOdqxkJCi2PiYB5rGS1jPYarhmwQ_9hvX5zPg4

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
