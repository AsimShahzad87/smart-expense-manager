from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        request: UserCreate,
    ) -> User:
        existing_user = UserRepository.get_by_email(
            db,
            request.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        user = User(
            email=request.email.lower(),
            password_hash=hash_password(
                request.password
            ),
            full_name=request.full_name.strip(),
            default_currency=request.default_currency.upper(),
        )

        return UserRepository.create(
            db,
            user,
        )

    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str,
    ) -> str:
        user = UserRepository.get_by_email(
            db,
            email.lower(),
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return create_access_token(
            str(user.id)
        )