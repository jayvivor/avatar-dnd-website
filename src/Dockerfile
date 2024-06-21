# Use an official Python runtime as the base image
FROM python:3.10

RUN apt install npm

RUN useradd -rm -d /app -s /bin/bash appuser
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app

# Install gcloud
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-480.0.0-linux-x86_64.tar.gz \
    && tar -xf google-cloud-cli-480.0.0-linux-x86_64.tar.gz \
    && google-cloud-sdk/install.sh --quiet

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

# # Copy the Django project files to the working directory
# COPY . /app

# Expose the port on which the Django app will run (default is 8000)
EXPOSE 8000

# # Run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]