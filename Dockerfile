# Python base image
FROM python:3.11-slim

# working directory in the container
WORKDIR /app

# requirements.txt 
COPY requirements.txt .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . .

# Expose the port 
EXPOSE 8000

# Set the command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
