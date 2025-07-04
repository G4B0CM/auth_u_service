class AuthException(Exception):
    """Base exception for authentication-related errors in the domain."""
    pass

class UserAlreadyExistsError(AuthException):
    """Raised when trying to register a user that already exists."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists.")

class InvalidCredentialsError(AuthException):
    """Raised when login fails due to incorrect email or password."""
    def __init__(self):
        super().__init__("Invalid email or password.")