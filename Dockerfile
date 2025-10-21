# Use the official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy all files to the working directory
COPY . .

# Install any dependencies
RUN pip install Flask --no-cache-dir -r requirements.txt



# Command to run on container start
CMD [ "python", "./app.py" ]

