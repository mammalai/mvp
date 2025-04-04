# Select a base image that includes Python
FROM python:3.11-slim

# Set up a working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject.toml and poetry.lock* files
COPY ./backend/pyproject.toml ./backend/poetry.lock* /app/

# Configure Poetry to not use a virtual environment in Docker
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the backend code 
COPY ./backend/ /app/backend/

# Expose the port the app runs on
EXPOSE 8080

# Set the command to run your FastAPI application with Uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8080"]

# For production, consider using Gunicorn with Uvicorn workers:
# CMD ["gunicorn", "backend.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
