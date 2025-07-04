from domain.repositories.user_repository import IUserRepository
from domain.exceptions.auth_exceptions import InvalidCredentialsError
from application.services.password_service import PasswordService
from application.services.jwt_service import JWTService

class LoginUserUseCase:
    def __init__(self, user_repository: IUserRepository, password_service: PasswordService, jwt_service: JWTService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.find_by_email(email)
        if not user or not self.password_service.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = self.jwt_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )
        return access_token