from fastapi import FastAPI
from api.v1 import auth_router
from core.config import settings
from infrastructure.database.connection import Base, engine

# This command will create the database tables if they don't exist.
# For production, you should use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Service",
    description="Service for user authentication and JWT management.",
    version="1.0.0"
)

# Include the router for version 1 of the auth API
app.include_router(auth_router.router, tags=["Authentication"])

@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}