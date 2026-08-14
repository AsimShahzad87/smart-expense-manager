from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
)
from app.services.auth_service import AuthService

from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    request: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register_user(
        db,
        request,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    access_token = AuthService.authenticate(
        db,
        request.email,
        request.password,
    )

    return TokenResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user