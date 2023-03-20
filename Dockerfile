FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose port 8000 for the Django development server
EXPOSE 8000

# Start the Django development server and the Node.js server
CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000 & npm start"]