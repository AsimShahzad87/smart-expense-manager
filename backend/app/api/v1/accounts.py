from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.account import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
)
from app.services.account_service import AccountService
from app.schemas.account import AccountBalanceResponse


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    request: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.create_account(
        db,
        current_user,
        request,
    )


@router.get(
    "",
    response_model=list[AccountResponse],
)
def get_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.get_accounts(
        db,
        current_user,
    )


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
)
def get_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.get_account(
        db,
        current_user,
        account_id,
    )


@router.get(
    "/{account_id}/balance",
    response_model=AccountBalanceResponse,
)
def get_account_balance(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.get_account_balance(
        db,
        current_user,
        account_id,
    )


@router.patch(
    "/{account_id}",
    response_model=AccountResponse,
)
def update_account(
    account_id: UUID,
    request: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.update_account(
        db,
        current_user,
        account_id,
        request,
    )


@router.delete(
    "/{account_id}",
    response_model=AccountResponse,
)
def deactivate_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService.deactivate_account(
        db,
        current_user,
        account_id,
    )