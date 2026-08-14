from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.enums import AccountNature, AccountType
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.account import (
    AccountBalanceResponse,
    AccountCreate,
    AccountUpdate,
)


class AccountService:

    @staticmethod
    def create_account(
        db: Session,
        current_user: User,
        request: AccountCreate,
    ) -> Account:

        account = Account(
            user_id=current_user.id,
            name=request.name.strip(),
            account_type=request.account_type,
            account_nature=request.account_nature,
            institution_name=request.institution_name,
            masked_account_number=request.masked_account_number,
            currency=request.currency.upper(),
            opening_balance=request.opening_balance,
            credit_limit=request.credit_limit,
            billing_day=request.billing_day,
            payment_due_day=request.payment_due_day,
        )

        return AccountRepository.create(
            db,
            account,
        )


    @staticmethod
    def get_accounts(
        db: Session,
        current_user: User,
    ) -> list[Account]:

        return AccountRepository.get_all_by_user(
            db,
            current_user.id,
        )


    @staticmethod
    def get_account(
        db: Session,
        current_user: User,
        account_id: UUID,
    ) -> Account:

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

        return account


    @staticmethod
    def update_account(
        db: Session,
        current_user: User,
        account_id: UUID,
        request: AccountUpdate,
    ) -> Account:

        account = AccountService.get_account(
            db,
            current_user,
            account_id,
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(account, field, value)

        if account.account_type == AccountType.CREDIT_CARD:
            if account.account_nature != AccountNature.LIABILITY:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Credit card accounts must have LIABILITY nature",
                )

            if account.credit_limit is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Credit limit is required for credit card accounts",
                )

        else:
            if account.credit_limit is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Credit limit is only allowed for credit card accounts",
                )

            if account.billing_day is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Billing day is only allowed for credit card accounts",
                )

            if account.payment_due_day is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Payment due day is only allowed for credit card accounts",
                )

        return AccountRepository.save(
            db,
            account,
        )
    

    @staticmethod
    def deactivate_account(
        db: Session,
        current_user: User,
        account_id: UUID,
    ) -> Account:

        account = AccountService.get_account(
            db,
            current_user,
            account_id,
        )

        account.is_active = False

        return AccountRepository.save(
            db,
            account,
        )

    
    @staticmethod
    def get_account_balance(
        db: Session,
        current_user: User,
        account_id: UUID,
    ) -> AccountBalanceResponse:
        account = AccountService.get_account(
            db,
            current_user,
            account_id,
        )

        # Credit card / liability account
        if account.account_type == AccountType.CREDIT_CARD:

            movement = (
                TransactionRepository
                .calculate_credit_card_movement(
                    db,
                    account.id,
                    current_user.id,
                )
            )

            outstanding = (
                account.opening_balance
                + movement
            )

            available_limit = None

            if account.credit_limit is not None:
                available_limit = (
                    account.credit_limit
                    - outstanding
                )

            return AccountBalanceResponse(
                account_id=account.id,
                account_name=account.name,
                account_type=account.account_type,
                account_nature=account.account_nature,
                currency=account.currency,
                opening_balance=account.opening_balance,
                current_balance=None,
                outstanding_balance=outstanding,
                credit_limit=account.credit_limit,
                available_limit=available_limit,
            )

        # Cash / Bank / Wallet / Other asset account
        movement = (
            TransactionRepository
            .calculate_account_net_movement(
                db,
                account.id,
                current_user.id,
            )
        )

        current_balance = (
            account.opening_balance
            + movement
        )

        return AccountBalanceResponse(
            account_id=account.id,
            account_name=account.name,
            account_type=account.account_type,
            account_nature=account.account_nature,
            currency=account.currency,
            opening_balance=account.opening_balance,
            current_balance=current_balance,
            outstanding_balance=None,
            credit_limit=None,
            available_limit=None,
        )