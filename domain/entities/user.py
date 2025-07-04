import uuid
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    """
    Represents the User entity within the domain.
    This is the pure business object, independent of any framework or database.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True # Allows creating Pydantic models from ORM objects