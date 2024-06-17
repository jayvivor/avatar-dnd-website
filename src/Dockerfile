# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Django project files to the working directory
COPY . /app

# Expose the port on which the Django app will run (default is 8000)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]