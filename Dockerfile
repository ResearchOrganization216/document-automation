# Using Python base image
FROM python:3.9-slim

# Setting the working directory
WORKDIR /app

# Copying dependencies
COPY requirements.txt requirements.txt

# Installing dependencies
RUN pip install -r requirements.txt

# Copying the application code
COPY . .

# Exposing Flask port
EXPOSE 5000

# Running the Flask app
CMD ["python", "run.py"]
