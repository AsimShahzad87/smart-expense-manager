from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from app.models.enums import TransactionType
from app.schemas.transaction import TransactionPageResponse

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    request: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.create_transaction(
        db,
        current_user,
        request,
    )


@router.get(
    "",
    response_model=TransactionPageResponse,
)
def get_transactions(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    transaction_type: TransactionType | None = Query(
        default=None,
        alias="type",
    ),
    account_id: UUID | None = Query(
        default=None,
    ),
    category_id: UUID | None = Query(
        default=None,
    ),
    date_from: date | None = Query(
        default=None,
    ),
    date_to: date | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.get_transactions(
        db=db,
        current_user=current_user,
        page=page,
        page_size=page_size,
        transaction_type=transaction_type,
        account_id=account_id,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.get_transaction(
        db,
        current_user,
        transaction_id,
    )


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: UUID,
    request: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.update_transaction(
        db,
        current_user,
        transaction_id,
        request,
    )


@router.delete(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService.delete_transaction(
        db,
        current_user,
        transaction_id,
    )