import pytest
import uuid
from application.use_cases.login_user import LoginUserUseCase
from domain.entities.user import User
from domain.exceptions.auth_exceptions import InvalidCredentialsError

def test_login_user_success(mock_user_repository, mock_password_service, mock_jwt_service):
    """Prueba el caso de éxito del login."""
    # Arrange
    use_case = LoginUserUseCase(mock_user_repository, mock_password_service, mock_jwt_service)
    email = "user@example.com"
    password = "password123"
    user_id = uuid.uuid4()
    
    user_in_db = User(id=user_id, email=email, hashed_password="hashed_password")
    mock_user_repository.find_by_email.return_value = user_in_db
    mock_password_service.verify_password.return_value = True
    mock_jwt_service.create_access_token.return_value = "fake.jwt.token"

    # Act
    token = use_case.execute(email, password)

    # Assert
    mock_user_repository.find_by_email.assert_called_once_with(email)
    mock_password_service.verify_password.assert_called_once_with(password, user_in_db.hashed_password)
    mock_jwt_service.create_access_token.assert_called_once_with(
        data={"sub": email, "user_id": str(user_id)}
    )
    assert token == "fake.jwt.token"

def test_login_user_wrong_password(mock_user_repository, mock_password_service, mock_jwt_service):
    """Prueba el login con contraseña incorrecta."""
    # Arrange
    use_case = LoginUserUseCase(mock_user_repository, mock_password_service, mock_jwt_service)
    email = "user@example.com"
    password = "wrong_password"
    
    user_in_db = User(id=uuid.uuid4(), email=email, hashed_password="hashed_password")
    mock_user_repository.find_by_email.return_value = user_in_db
    mock_password_service.verify_password.return_value = False

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        use_case.execute(email, password)
    
    mock_jwt_service.create_access_token.assert_not_called()

def test_login_user_not_found(mock_user_repository, mock_password_service, mock_jwt_service):
    """Prueba el login de un usuario que no existe."""
    # Arrange
    use_case = LoginUserUseCase(mock_user_repository, mock_password_service, mock_jwt_service)
    mock_user_repository.find_by_email.return_value = None

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        use_case.execute("nonexistent@example.com", "password")

    mock_password_service.verify_password.assert_not_called()