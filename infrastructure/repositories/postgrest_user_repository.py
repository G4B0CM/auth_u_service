from typing import Optional
import uuid
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.repositories.user_repository import IUserRepository
from infrastructure.database.models import UserDB

class PostgresUserRepository(IUserRepository):
    """
    Concrete implementation of the IUserRepository using PostgreSQL and SQLAlchemy.
    This class is responsible for mapping between the domain User entity and
    the infrastructure UserDB ORM model.
    """
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_entity(self, user_db: UserDB) -> User:
        """Maps a UserDB ORM object to a User domain entity."""
        return User(
            id=user_db.id,
            email=user_db.email,
            hashed_password=user_db.hashed_password
        )

    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        user_db = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        return self._to_entity(user_db) if user_db else None

    def find_by_email(self, email: str) -> Optional[User]:
        user_db = self.db.query(UserDB).filter(UserDB.email == email).first()
        return self._to_entity(user_db) if user_db else None

    def save(self, user: User) -> User:
        user_db = self.db.query(UserDB).filter(UserDB.id == user.id).first()
        if not user_db:
            user_db = UserDB(id=user.id)
        
        user_db.email = user.email
        user_db.hashed_password = user.hashed_password
        
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        
        return self._to_entity(user_db)