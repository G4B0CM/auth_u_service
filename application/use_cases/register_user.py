from domain.entities.user import User
from domain.repositories.user_repository import IUserRepository
from domain.exceptions.auth_exceptions import UserAlreadyExistsError
from application.services.password_service import PasswordService

class RegisterUserUseCase:
    def __init__(self, user_repository: IUserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(self, email: str, password: str) -> User:
        if self.user_repository.find_by_email(email):
            raise UserAlreadyExistsError(email)

        hashed_password = self.password_service.get_password_hash(password)
        new_user = User(email=email, hashed_password=hashed_password)
        
        return self.user_repository.save(new_user)