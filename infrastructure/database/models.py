import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.database.connection import Base

class UserDB(Base):
    """
    SQLAlchemy ORM model for the 'users' table.
    This is an infrastructure detail, separate from the domain entity.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)