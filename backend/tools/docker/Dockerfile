# Select a base image that includes Python
FROM python:3.11-slim

# Set up a working directory in the container for your application
WORKDIR /run

# Copy the backend code into the container
COPY ./backend/ /run/backend

# Install any Python dependencies listed in 'requirements.txt'
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Set the command to run your application
# (Be sure to replace './your_app_script.py' with the relative path to the Python file that starts your application)
# PROD
# gunicorn -b 0.0.0.0:8000 'backend.app:create_app()'
CMD ["gunicorn", "-b", "0.0.0.0:8080", "backend.app:create_app()"]

# CMD ["flask", "run", "--host=0.0.0.0", "--debug"]