# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /home/kitsu

# Copy the current directory contents into the container at /app
ADD source /home/kitsu
ADD Requirements /home/kitsu/requirements

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /home/kitsu/requirements/development.txt
# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP Flask_Base

# Run app.py when the container launches
CMD ["python", "mainapp.py"]

