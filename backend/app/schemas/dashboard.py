from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import AccountNature, AccountType


class DashboardAccountBalance(BaseModel):
    account_id: UUID
    account_name: str
    account_type: AccountType
    account_nature: AccountNature
    currency: str

    current_balance: Decimal | None = None
    outstanding_balance: Decimal | None = None

    credit_limit: Decimal | None = None
    available_limit: Decimal | None = None


class DashboardSummaryResponse(BaseModel):
    currency: str

    total_assets: Decimal
    total_liabilities: Decimal
    net_worth: Decimal

    monthly_income: Decimal
    monthly_expenses: Decimal
    monthly_refunds: Decimal
    monthly_net: Decimal

    accounts: list[DashboardAccountBalance]