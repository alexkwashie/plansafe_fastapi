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

# Run uvicorn on the correct port
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]