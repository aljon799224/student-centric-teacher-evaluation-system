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




# # for deployment
# # Use the official Python slim image
# FROM python:3.12-slim
#
# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
# # Set working directory
# WORKDIR /app
#
# # Install system dependencies (for psycopg2 and others)
# RUN apt-get update && apt-get install -y \
#     build-essential libpq-dev curl && \
#     apt-get clean
#
# # Copy Poetry config and install dependencies
# COPY pyproject.toml poetry.lock ./
# RUN pip install --upgrade pip && pip install poetry
# RUN poetry config virtualenvs.create false \
#  && poetry install --no-root --only main
#
# # Copy the rest of the application code
# COPY . .
#
# # Expose FastAPI port
# EXPOSE 8000
#
# # Run migrations and start FastAPI (no --reload in production)
# CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"]
