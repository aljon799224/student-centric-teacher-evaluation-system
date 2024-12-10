# Use the official Python image as a base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy only the dependency files first
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install --upgrade pip
# RUN pip install poetry && poetry install --no-dev
RUN pip install poetry && poetry install --no-root --with dev

# Copy the rest of the application code
COPY . .

# Expose the FastAPI application port
EXPOSE 8000

# Command to run the application
CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]