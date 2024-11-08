# Use Python 3.12 base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the entire test framework code into the container
COPY . .

# Run pytest to execute the tests
CMD ["/bin/bash"]