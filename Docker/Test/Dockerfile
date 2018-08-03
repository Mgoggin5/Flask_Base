# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /usr/local/kitsu

RUN apt-get update 

# Copy the current directory contents into the container at /app
ADD source /usr/local/kitsu
ADD Requirements /usr/local/kitsu/requirements
COPY scripts/test.sh /usr/local/bin
RUN chmod +x /usr/local/bin/test.sh

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /usr/local/kitsu/requirements/development.txt
# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP kitsu.py

# Initializing flask app 
ENTRYPOINT ["test.sh"]

