# Use the official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and Node.js
RUN apt-get update && apt-get install -y \
    python3-pip \
    nodejs \
    npm \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY backend/app/requirements.txt /app/backend/app/
RUN pip3 install -r /app/backend/app/requirements.txt

# Install Node.js dependencies
COPY frontend/package.json /app/frontend/
COPY frontend/package-lock.json /app/frontend/
RUN cd /app/frontend && npm install

# Expose ports
EXPOSE 8000
EXPOSE 3000

# Start script will be provided by docker-compose.yml
CMD ["sh", "-c", "echo 'Please specify the service to start: backend or frontend'"]
