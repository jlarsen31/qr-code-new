# Use the official Python image as the parent image
FROM python:3.8-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required libraries
RUN pip3 install --no-cache-dir -r requirements.txt 

# Create Statid Dir
RUN mkdir static

# Copy the application code into the container
COPY app.py .
ADD templates ./templates

# Start the Flask application
#CMD ["python3", "app.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]