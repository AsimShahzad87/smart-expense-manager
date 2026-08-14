from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.category import Category
from app.models.enums import (
    CategoryType,
    TransactionType,
)
from app.models.transaction import Transaction
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)


class TransactionService:

    @staticmethod
    def _get_account(
        db: Session,
        current_user: User,
        account_id: UUID | None,
    ) -> Account | None:

        if account_id is None:
            return None

        account = AccountRepository.get_by_id_and_user(
            db,
            account_id,
            current_user.id,
        )

        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found",
            )

        if not account.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive account cannot be used",
            )

        return account

    @staticmethod
    def _get_category(
        db: Session,
        current_user: User,
        category_id: UUID | None,
    ) -> Category | None:

        if category_id is None:
            return None

        category = CategoryRepository.get_by_id(
            db,
            category_id,
            current_user.id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        if not category.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive category cannot be used",
            )

        return category

    @staticmethod
    def _validate_transaction(
        transaction_type: TransactionType,
        source_account: Account | None,
        destination_account: Account | None,
        category: Category | None,
        currency: str,
    ) -> None:

        if transaction_type == TransactionType.EXPENSE:

            if source_account is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source account is required for an expense",
                )

            if destination_account is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Destination account is not allowed for an expense",
                )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is required for an expense",
                )

            if category.category_type not in (
                CategoryType.EXPENSE,
                CategoryType.BOTH,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Selected category cannot be used for an expense",
                )

        elif transaction_type == TransactionType.INCOME:

            if destination_account is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Destination account is required for income",
                )

            if source_account is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source account is not allowed for income",
                )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is required for income",
                )

            if category.category_type not in (
                CategoryType.INCOME,
                CategoryType.BOTH,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Selected category cannot be used for income",
                )

        elif transaction_type == TransactionType.TRANSFER:

            if source_account is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source account is required for a transfer",
                )

            if destination_account is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Destination account is required for a transfer",
                )

            if source_account.id == destination_account.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source and destination accounts must be different",
                )

            if category is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is not allowed for a transfer",
                )

        elif transaction_type == TransactionType.REFUND:

            if destination_account is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Destination account is required for a refund",
                )

            if source_account is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source account is not allowed for a refund",
                )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category is required for a refund",
                )

            if category.category_type not in (
                CategoryType.EXPENSE,
                CategoryType.BOTH,
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Refund category must be an expense category",
                )

        accounts = [
            account
            for account in (
                source_account,
                destination_account,
            )
            if account is not None
        ]

        for account in accounts:
            if account.currency.upper() != currency.upper():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Transaction currency {currency.upper()} "
                        f"does not match account currency "
                        f"{account.currency.upper()}"
                    ),
                )

    @staticmethod
    def create_transaction(
        db: Session,
        current_user: User,
        request: TransactionCreate,
    ) -> Transaction:

        source_account = TransactionService._get_account(
            db,
            current_user,
            request.source_account_id,
        )

        destination_account = TransactionService._get_account(
            db,
            current_user,
            request.destination_account_id,
        )

        category = TransactionService._get_category(
            db,
            current_user,
            request.category_id,
        )

        currency = request.currency.upper()

        TransactionService._validate_transaction(
            request.type,
            source_account,
            destination_account,
            category,
            currency,
        )

        transaction = Transaction(
            user_id=current_user.id,
            type=request.type,

            source_account_id=(
                source_account.id
                if source_account
                else None
            ),

            destination_account_id=(
                destination_account.id
                if destination_account
                else None
            ),

            category_id=(
                category.id
                if category
                else None
            ),

            amount=request.amount,
            currency=currency,

            merchant=(
                request.merchant.strip()
                if request.merchant
                else None
            ),

            description=(
                request.description.strip()
                if request.description
                else None
            ),

            notes=request.notes,

            source=request.source,
            transaction_date=request.transaction_date,
        )

        return TransactionRepository.create(
            db,
            transaction,
        )

    @staticmethod
    def get_transactions(
        db: Session,
        current_user: User,
    ) -> list[Transaction]:

        return TransactionRepository.get_all_by_user(
            db,
            current_user.id,
        )

    @staticmethod
    def get_transaction(
        db: Session,
        current_user: User,
        transaction_id: UUID,
    ) -> Transaction:

        transaction = (
            TransactionRepository.get_by_id_and_user(
                db,
                transaction_id,
                current_user.id,
            )
        )

        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )

        return transaction

    @staticmethod
    def update_transaction(
        db: Session,
        current_user: User,
        transaction_id: UUID,
        request: TransactionUpdate,
    ) -> Transaction:

        transaction = TransactionService.get_transaction(
            db,
            current_user,
            transaction_id,
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        transaction_type = update_data.get(
            "type",
            transaction.type,
        )

        source_account_id = update_data.get(
            "source_account_id",
            transaction.source_account_id,
        )

        destination_account_id = update_data.get(
            "destination_account_id",
            transaction.destination_account_id,
        )

        category_id = update_data.get(
            "category_id",
            transaction.category_id,
        )

        currency = update_data.get(
            "currency",
            transaction.currency,
        ).upper()

        source_account = TransactionService._get_account(
            db,
            current_user,
            source_account_id,
        )

        destination_account = TransactionService._get_account(
            db,
            current_user,
            destination_account_id,
        )

        category = TransactionService._get_category(
            db,
            current_user,
            category_id,
        )

        TransactionService._validate_transaction(
            transaction_type,
            source_account,
            destination_account,
            category,
            currency,
        )

        for field, value in update_data.items():

            if field == "currency" and value is not None:
                value = value.upper()

            if field in (
                "merchant",
                "description",
            ) and value is not None:
                value = value.strip()

            setattr(
                transaction,
                field,
                value,
            )

        return TransactionRepository.save(
            db,
            transaction,
        )


    @staticmethod
    def delete_transaction(
        db: Session,
        current_user: User,
        transaction_id: UUID,
    ) -> Transaction:

        transaction = TransactionService.get_transaction(
            db,
            current_user,
            transaction_id,
        )

        transaction.deleted_at = datetime.now(
            timezone.utc
        )

        return TransactionRepository.save(
            db,
            transaction,
        )