from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TransactionSource, TransactionType


class TransactionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: TransactionType

    source_account_id: UUID | None = None
    destination_account_id: UUID | None = None
    category_id: UUID | None = None

    amount: Decimal = Field(gt=0)

    currency: str = Field(
        default="PKR",
        min_length=3,
        max_length=3,
    )

    merchant: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = None

    source: TransactionSource = TransactionSource.MANUAL

    transaction_date: datetime


class TransactionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: TransactionType | None = None

    source_account_id: UUID | None = None
    destination_account_id: UUID | None = None
    category_id: UUID | None = None

    amount: Decimal | None = Field(
        default=None,
        gt=0,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    merchant: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = None

    transaction_date: datetime | None = None


class TransactionResponse(BaseModel):
    id: UUID

    type: TransactionType

    source_account_id: UUID | None
    destination_account_id: UUID | None
    category_id: UUID | None

    amount: Decimal
    currency: str

    merchant: str | None
    description: str | None
    notes: str | None

    source: TransactionSource
    transaction_date: datetime

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TransactionPageResponse(BaseModel):
    items: list[TransactionResponse]

    page: int
    page_size: int

    total_items: int
    total_pages: int