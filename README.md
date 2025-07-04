# Auth Service

## Overview

The **Auth Service** is a core microservice responsible for user authentication and authorization within the Automated Cyber Risk Assessment Platform. It handles user registration, login, and the issuance of JSON Web Tokens (JWTs) to secure communication with other services.

This service is built using Python with the FastAPI framework and follows **Clean Architecture** principles to ensure separation of concerns, testability, and maintainability.

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** JWT (python-jose), Passlib (for password hashing)
- **Containerization:** Docker

## Architecture

The service is structured into four distinct layers:

1.  **Domain:** Contains the core business logic, entities (e.g., `User`), and abstract repository interfaces. It has zero dependencies on other layers.
2.  **Application:** Contains the application-specific use cases (e.g., `RegisterUserUseCase`, `LoginUserUseCase`) that orchestrate the flow of data between the domain and infrastructure layers.
3.  **Infrastructure:** Provides concrete implementations for the abstractions defined in the domain layer, such as the PostgreSQL repository, database connection, and ORM models.
4.  **API (Presentation):** The entry point to the application. It consists of the FastAPI routers and schemas, responsible for handling HTTP requests and responses.

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL instance

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd auth-service
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Copy the example `.env` file and fill in your configuration details.
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file with your database URL, secret key, etc.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000` and the interactive documentation at `http://127.0.0.1:8000/docs`.

### Running with Docker

1.  Ensure you have a `.env` file configured.
2.  Build and run the Docker container:
    ```bash
    docker build -t auth-service .
    docker run --env-file .env -p 8000:8000 auth-service
    ```
    *Note: For the container to connect to a database on your host machine, you may need to use `host.docker.internal` instead of `localhost` in your `DATABASE_URL`.*

## API Endpoints

### Register a new user

- **URL:** `/api/v1/auth/register`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "test@example.com",
    "password": "a-strong-password"
  }

### Success Response (201):
Generated json
{
  "id": "some-uuid",
  "email": "test@example.com"
}

### Login a user
URL: /api/v1/auth/login
Method: POST
Request Body:
Generated json
{
  "email": "test@example.com",
  "password": "a-strong-password"
}

Success Response (200):
Generated json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}

**`auth-service/.env.example`**
```ini
# PostgreSQL Database URL
# Format: postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/auth_db"

# JWT Settings
SECRET_KEY="a_very_secret_key_that_should_be_long_and_random"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30