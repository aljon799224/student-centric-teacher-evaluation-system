# **FastAPI with PostgreSQL, Docker, and Poetry**

## **Overview**
This project is a fully containerized FastAPI application built using PostgreSQL for its database, 
Docker for containerization, and Poetry for Python dependency management.

The project includes a pre-configured Docker Compose setup for managing services, a .env file for 
handling environment variables, and GitHub Actions for continuous integration (CI). The GitHub Actions workflow 
runs tests, checks code coverage, and ensures code quality automatically on every commit or pull request, 
providing a seamless CI/CD pipeline for your FastAPI application.

**Prerequisites**

Make sure you have the following installed:
- **Docker**: Install Docker
- **Docker Compose**: Install Docker Compose
- **Poetry**: Install Poetry
   ```commandline
   pip install poetry

## **How to Run the Project**

## **Environment Variables**

Set the following environment variables by either exporting them locally or 
creating a .env file in the root directory:

**Example**

```doctest
SQLALCHEMY_DATABASE_URL=postgresql://user:password@db:5432/db
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=db
PGADMIN_DEFAULT_EMAIL=admin@yahoo.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## **Run the Application**
1. Build and start Docker containers:
    ```commandline 
   docker compose up --build

2. Access FastAPI documentation: Open your browser and go to:
    ```commandline 
   http://localhost:8000/docs

## **How to Run Pre-commit Hooks**
Pre-commit hooks ensure code quality before commits. Here's how to set them up and run them:

1. Install pre-commit hooks: Set up the git hook scripts with:
    ```commandline 
   pre-commit install

2. Run pre-commit on all files: Manually run the pre-commit hooks on all files with:
    ```commandline 
   pre-commit run --all-files
## **How to Run Unit Tests**

Run the unit tests with coverage using the following command:

1. Exec into the container:
    ```commandline 
   docker compose exec <container-id> bash -it

2. Start the Poetry shell:
    ```commandline 
   poetry shell

3. Run the tests:
    ```commandline 
   pytest --cov=app --cov-report=html:htmlcov --cov-report=term-missing -vv

This will execute the tests and display a coverage report, including any lines not covered.

# **Additional Information**
- **Database Access**: You can use pgAdmin or any preferred PostgreSQL client to manage the database.
- **Environment Variables**: Ensure that the .env file contains all necessary environment variables for
database connection and other services.
