import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.enums import TransactionSource, TransactionType

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)


class Transaction(Base):
    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_transactions_amount_positive",
        ),
        CheckConstraint(
            """
            type != 'TRANSFER'
            OR (
                source_account_id IS NOT NULL
                AND destination_account_id IS NOT NULL
                AND source_account_id <> destination_account_id
            )
            """,
            name="ck_transactions_transfer_accounts",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum"),
        nullable=False,
    )

    source_account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    destination_account_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="PKR",
    )

    merchant: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source: Mapped[TransactionSource] = mapped_column(
        Enum(TransactionSource, name="transaction_source_enum"),
        nullable=False,
        default=TransactionSource.MANUAL,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )