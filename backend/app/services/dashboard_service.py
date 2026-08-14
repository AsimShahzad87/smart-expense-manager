from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.enums import AccountNature, AccountType
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.dashboard import (
    DashboardAccountBalance,
    DashboardSummaryResponse,
)


class DashboardService:

    @staticmethod
    def get_summary(
        db: Session,
        current_user: User,
    ) -> DashboardSummaryResponse:

        now = datetime.now(timezone.utc)

        month_start = datetime(
            year=now.year,
            month=now.month,
            day=1,
            tzinfo=timezone.utc,
        )

        if now.month == 12:
            next_month_start = datetime(
                year=now.year + 1,
                month=1,
                day=1,
                tzinfo=timezone.utc,
            )
        else:
            next_month_start = datetime(
                year=now.year,
                month=now.month + 1,
                day=1,
                tzinfo=timezone.utc,
            )

        accounts = AccountRepository.get_active_by_user(
            db,
            current_user.id,
        )

        total_assets = Decimal("0.00")
        total_liabilities = Decimal("0.00")

        account_balances: list[DashboardAccountBalance] = []

        for account in accounts:

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

                total_liabilities += outstanding

                account_balances.append(
                    DashboardAccountBalance(
                        account_id=account.id,
                        account_name=account.name,
                        account_type=account.account_type,
                        account_nature=account.account_nature,
                        currency=account.currency,
                        current_balance=None,
                        outstanding_balance=outstanding,
                        credit_limit=account.credit_limit,
                        available_limit=available_limit,
                    )
                )

            else:

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

                if account.account_nature == AccountNature.ASSET:
                    total_assets += current_balance

                account_balances.append(
                    DashboardAccountBalance(
                        account_id=account.id,
                        account_name=account.name,
                        account_type=account.account_type,
                        account_nature=account.account_nature,
                        currency=account.currency,
                        current_balance=current_balance,
                        outstanding_balance=None,
                        credit_limit=None,
                        available_limit=None,
                    )
                )

        monthly_income = (
            TransactionRepository.get_monthly_income(
                db,
                current_user.id,
                month_start,
                next_month_start,
            )
        )

        monthly_expenses = (
            TransactionRepository.get_monthly_expenses(
                db,
                current_user.id,
                month_start,
                next_month_start,
            )
        )

        monthly_refunds = (
            TransactionRepository.get_monthly_refunds(
                db,
                current_user.id,
                month_start,
                next_month_start,
            )
        )

        net_monthly_expenses = (
            monthly_expenses
            - monthly_refunds
        )

        monthly_net = (
            monthly_income
            - net_monthly_expenses
        )

        net_worth = (
            total_assets
            - total_liabilities
        )

        return DashboardSummaryResponse(
            currency=current_user.default_currency,

            total_assets=total_assets,
            total_liabilities=total_liabilities,
            net_worth=net_worth,

            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            monthly_refunds=monthly_refunds,
            monthly_net=monthly_net,

            accounts=account_balances,
        )