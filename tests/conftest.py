import pytest
from unittest.mock import MagicMock
from domain.repositories.user_repository import IUserRepository
from application.services.password_service import PasswordService
from application.services.jwt_service import JWTService

@pytest.fixture
def mock_user_repository(mocker):
    """Fixture para mockear el repositorio de usuarios."""
    return mocker.MagicMock(spec=IUserRepository)

@pytest.fixture
def mock_password_service(mocker):
    """Fixture para mockear el servicio de contraseñas."""
    return mocker.MagicMock(spec=PasswordService)

@pytest.fixture
def mock_jwt_service(mocker):
    """Fixture para mockear el servicio de JWT."""
    return mocker.MagicMock(spec=JWTService)