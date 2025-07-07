import pytest
import uuid
from application.use_cases.register_user import RegisterUserUseCase
from domain.entities.user import User
from domain.exceptions.auth_exceptions import UserAlreadyExistsError

def test_register_user_success(mock_user_repository, mock_password_service):
    """Prueba el caso de éxito del registro de un nuevo usuario."""
    # Arrange
    use_case = RegisterUserUseCase(mock_user_repository, mock_password_service)
    email = "newuser@example.com"
    password = "a-strong-password"
    hashed_password = "hashed_password_string"
    
    mock_user_repository.find_by_email.return_value = None
    mock_password_service.get_password_hash.return_value = hashed_password
    
    # Simula que el método save devuelve el usuario con un ID
    def save_side_effect(user):
        user.id = uuid.uuid4()
        return user
    mock_user_repository.save.side_effect = save_side_effect

    # Act
    created_user = use_case.execute(email, password)

    # Assert
    mock_user_repository.find_by_email.assert_called_once_with(email)
    mock_password_service.get_password_hash.assert_called_once_with(password)
    mock_user_repository.save.assert_called_once()
    
    saved_user_arg = mock_user_repository.save.call_args[0][0]
    assert isinstance(saved_user_arg, User)
    assert saved_user_arg.email == email
    assert saved_user_arg.hashed_password == hashed_password
    
    assert created_user.email == email

def test_register_user_already_exists(mock_user_repository, mock_password_service):
    """Prueba que se lanza una excepción si el usuario ya existe."""
    # Arrange
    use_case = RegisterUserUseCase(mock_user_repository, mock_password_service)
    email = "existing@example.com"
    password = "a-strong-password"
    
    mock_user_repository.find_by_email.return_value = User(
        email=email, hashed_password="some_hash"
    )

    # Act & Assert
    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(email, password)

    mock_user_repository.find_by_email.assert_called_once_with(email)
    mock_password_service.get_password_hash.assert_not_called()
    mock_user_repository.save.assert_not_called()