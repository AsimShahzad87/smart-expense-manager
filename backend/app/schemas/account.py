from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import AccountNature, AccountType


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    account_type: AccountType
    account_nature: AccountNature

    institution_name: str | None = Field(default=None, max_length=150)
    masked_account_number: str | None = Field(default=None, max_length=50)

    currency: str = Field(default="PKR", min_length=3, max_length=3)
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0)

    credit_limit: Decimal | None = Field(default=None, gt=0)
    billing_day: int | None = Field(default=None, ge=1, le=31)
    payment_due_day: int | None = Field(default=None, ge=1, le=31)

    @model_validator(mode="after")
    def validate_account_rules(self):
        if self.account_type == AccountType.CREDIT_CARD:
            if self.account_nature != AccountNature.LIABILITY:
                raise ValueError(
                    "Credit card accounts must have LIABILITY nature"
                )

            if self.credit_limit is None:
                raise ValueError(
                    "Credit limit is required for credit card accounts"
                )

        else:
            if self.account_nature != AccountNature.ASSET:
                raise ValueError(
                    "Non-credit-card accounts must have ASSET nature"
                )

            if self.credit_limit is not None:
                raise ValueError(
                    "Credit limit is only allowed for credit card accounts"
                )

            if self.billing_day is not None:
                raise ValueError(
                    "Billing day is only allowed for credit card accounts"
                )

            if self.payment_due_day is not None:
                raise ValueError(
                    "Payment due day is only allowed for credit card accounts"
                )

        return self


class AccountUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    institution_name: str | None = Field(default=None, max_length=150)
    masked_account_number: str | None = Field(default=None, max_length=50)

    opening_balance: Decimal | None = Field(default=None, ge=0)

    credit_limit: Decimal | None = Field(default=None, gt=0)
    billing_day: int | None = Field(default=None, ge=1, le=31)
    payment_due_day: int | None = Field(default=None, ge=1, le=31)

    is_active: bool | None = None


class AccountResponse(BaseModel):
    id: UUID
    name: str
    account_type: AccountType
    account_nature: AccountNature

    institution_name: str | None
    masked_account_number: str | None

    currency: str
    opening_balance: Decimal

    credit_limit: Decimal | None
    billing_day: int | None
    payment_due_day: int | None

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )