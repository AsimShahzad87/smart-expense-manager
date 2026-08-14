"""seed system categories

Revision ID: 706e5c982fac
Revises: 6cc3b1c2892d
Create Date: 2026-08-14 23:23:12.085146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision: str = '706e5c982fac'
down_revision: Union[str, Sequence[str], None] = '6cc3b1c2892d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    now = datetime.now(timezone.utc)

    categories_table = sa.table(
        "categories",

        sa.column("id", sa.UUID()),
        sa.column("user_id", sa.UUID()),
        sa.column("name", sa.String()),
        sa.column(
            "category_type",
            sa.Enum(
                "INCOME",
                "EXPENSE",
                "BOTH",
                name="category_type_enum",
                create_type=False,
            ),
        ),
        sa.column("icon", sa.String()),
        sa.column("is_system", sa.Boolean()),
        sa.column("is_active", sa.Boolean()),
        sa.column(
            "created_at",
            sa.DateTime(timezone=True),
        ),
        sa.column(
            "updated_at",
            sa.DateTime(timezone=True),
        ),
    )

    op.bulk_insert(
        categories_table,
        [
            {
                "id": "10000000-0000-0000-0000-000000000001",
                "user_id": None,
                "name": "Food & Dining",
                "category_type": "EXPENSE",
                "icon": "food_dining",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000002",
                "user_id": None,
                "name": "Groceries",
                "category_type": "EXPENSE",
                "icon": "groceries",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000003",
                "user_id": None,
                "name": "Transport",
                "category_type": "EXPENSE",
                "icon": "transport",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000004",
                "user_id": None,
                "name": "Fuel",
                "category_type": "EXPENSE",
                "icon": "fuel",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000005",
                "user_id": None,
                "name": "Shopping",
                "category_type": "EXPENSE",
                "icon": "shopping",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000006",
                "user_id": None,
                "name": "Utilities",
                "category_type": "EXPENSE",
                "icon": "utilities",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000007",
                "user_id": None,
                "name": "Rent",
                "category_type": "EXPENSE",
                "icon": "rent",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000008",
                "user_id": None,
                "name": "Education",
                "category_type": "EXPENSE",
                "icon": "education",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000009",
                "user_id": None,
                "name": "Healthcare",
                "category_type": "EXPENSE",
                "icon": "healthcare",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000010",
                "user_id": None,
                "name": "Entertainment",
                "category_type": "EXPENSE",
                "icon": "entertainment",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000011",
                "user_id": None,
                "name": "Travel",
                "category_type": "EXPENSE",
                "icon": "travel",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000012",
                "user_id": None,
                "name": "Subscriptions",
                "category_type": "EXPENSE",
                "icon": "subscriptions",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000013",
                "user_id": None,
                "name": "Personal Care",
                "category_type": "EXPENSE",
                "icon": "personal_care",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000014",
                "user_id": None,
                "name": "Gifts & Donations",
                "category_type": "EXPENSE",
                "icon": "gifts",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "10000000-0000-0000-0000-000000000015",
                "user_id": None,
                "name": "Other Expense",
                "category_type": "EXPENSE",
                "icon": "other_expense",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },

            # INCOME

            {
                "id": "20000000-0000-0000-0000-000000000001",
                "user_id": None,
                "name": "Salary",
                "category_type": "INCOME",
                "icon": "salary",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "20000000-0000-0000-0000-000000000002",
                "user_id": None,
                "name": "Business",
                "category_type": "INCOME",
                "icon": "business",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "20000000-0000-0000-0000-000000000003",
                "user_id": None,
                "name": "Freelance",
                "category_type": "INCOME",
                "icon": "freelance",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "20000000-0000-0000-0000-000000000004",
                "user_id": None,
                "name": "Investment",
                "category_type": "INCOME",
                "icon": "investment",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "20000000-0000-0000-0000-000000000005",
                "user_id": None,
                "name": "Gift Received",
                "category_type": "INCOME",
                "icon": "gift_received",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": "20000000-0000-0000-0000-000000000006",
                "user_id": None,
                "name": "Other Income",
                "category_type": "INCOME",
                "icon": "other_income",
                "is_system": True,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:

    system_category_ids = [
        "10000000-0000-0000-0000-000000000001",
        "10000000-0000-0000-0000-000000000002",
        "10000000-0000-0000-0000-000000000003",
        "10000000-0000-0000-0000-000000000004",
        "10000000-0000-0000-0000-000000000005",
        "10000000-0000-0000-0000-000000000006",
        "10000000-0000-0000-0000-000000000007",
        "10000000-0000-0000-0000-000000000008",
        "10000000-0000-0000-0000-000000000009",
        "10000000-0000-0000-0000-000000000010",
        "10000000-0000-0000-0000-000000000011",
        "10000000-0000-0000-0000-000000000012",
        "10000000-0000-0000-0000-000000000013",
        "10000000-0000-0000-0000-000000000014",
        "10000000-0000-0000-0000-000000000015",

        "20000000-0000-0000-0000-000000000001",
        "20000000-0000-0000-0000-000000000002",
        "20000000-0000-0000-0000-000000000003",
        "20000000-0000-0000-0000-000000000004",
        "20000000-0000-0000-0000-000000000005",
        "20000000-0000-0000-0000-000000000006",
    ]

    categories = sa.table(
        "categories",
        sa.column("id", sa.UUID()),
    )

    op.execute(
        categories.delete().where(
            categories.c.id.in_(system_category_ids)
        )
    )
