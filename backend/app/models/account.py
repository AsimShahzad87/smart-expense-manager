import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.enums import AccountNature, AccountType

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)


class Account(Base):
    __tablename__ = "accounts"

    __table_args__ = (
        CheckConstraint(
            "opening_balance >= 0",
            name="ck_accounts_opening_balance_non_negative",
        ),
        CheckConstraint(
            "credit_limit IS NULL OR credit_limit > 0",
            name="ck_accounts_credit_limit_positive",
        ),
        CheckConstraint(
            "billing_day IS NULL OR billing_day BETWEEN 1 AND 31",
            name="ck_accounts_billing_day",
        ),
        CheckConstraint(
            "payment_due_day IS NULL OR payment_due_day BETWEEN 1 AND 31",
            name="ck_accounts_payment_due_day",
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

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    account_type: Mapped[AccountType] = mapped_column(
        Enum(AccountType, name="account_type_enum"),
        nullable=False,
    )

    account_nature: Mapped[AccountNature] = mapped_column(
        Enum(AccountNature, name="account_nature_enum"),
        nullable=False,
    )

    institution_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    masked_account_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="PKR",
    )

    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    credit_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )

    billing_day: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    payment_due_day: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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