from abc import ABC, abstractmethod
from typing import Optional
import uuid

from domain.entities.user import User

class IUserRepository(ABC):
    """
    Defines the interface (Port) for a user repository.
    This abstract class lives in the domain layer and dictates the contract
    that any data persistence implementation must adhere to.
    """

    @abstractmethod
    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Finds a user by their unique ID."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user by their email address."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Saves a user entity (creates or updates)."""
        pass