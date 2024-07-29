# Use the official Ubuntu image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and required dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    postgresql-client \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY app/requirements.txt /app/app/
RUN pip3 install -r /app/app/requirements.txt

# Install Jupyter Notebook
RUN pip3 install jupyter

# Copy the rest of the application code
COPY . /app

# Expose ports for FastAPI and Jupyter Notebook
EXPOSE 8000 8888
