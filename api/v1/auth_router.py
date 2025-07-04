from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.v1 import schemas
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.login_user import LoginUserUseCase
from application.services.password_service import PasswordService
from application.services.jwt_service import JWTService
from domain.exceptions.auth_exceptions import UserAlreadyExistsError, InvalidCredentialsError
from infrastructure.database.connection import get_db
from infrastructure.repositories.postgres_user_repository import PostgresUserRepository

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Handles the user registration request.
    This endpoint wires together the dependencies for the RegisterUserUseCase.
    """
    user_repo = PostgresUserRepository(db)
    password_service = PasswordService()
    use_case = RegisterUserUseCase(user_repo, password_service)
    
    try:
        created_user = use_case.execute(email=user.email, password=user.password)
        return created_user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Handles the user login request and returns a JWT.
    """
    user_repo = PostgresUserRepository(db)
    password_service = PasswordService()
    jwt_service = JWTService()
    use_case = LoginUserUseCase(user_repo, password_service, jwt_service)

    try:
        access_token = use_case.execute(email=user.email, password=user.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )