# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY keys/ .
COPY config.ini .
COPY .env .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY smartparent/ .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "smartparent.wsgi:application"]