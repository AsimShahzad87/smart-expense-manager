from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.enums import TransactionType
from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(
        db: Session,
        transaction: Transaction,
    ) -> Transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: UUID,
    ) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(
                Transaction.user_id == user_id,
                Transaction.deleted_at.is_(None),
            )
            .order_by(
                Transaction.transaction_date.desc()
            )
        )

        return list(
            db.execute(statement)
            .scalars()
            .all()
        )

    @staticmethod
    def get_by_id_and_user(
        db: Session,
        transaction_id: UUID,
        user_id: UUID,
    ) -> Transaction | None:
        statement = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id,
            Transaction.deleted_at.is_(None),
        )

        return db.execute(
            statement
        ).scalar_one_or_none()

    @staticmethod
    def save(
        db: Session,
        transaction: Transaction,
    ) -> Transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def calculate_account_net_movement(
        db: Session,
        account_id: UUID,
        user_id: UUID,
    ):
        statement = select(
            func.coalesce(
                func.sum(
                    case(
                        (
                            Transaction.destination_account_id == account_id,
                            Transaction.amount,
                        ),
                        (
                            Transaction.source_account_id == account_id,
                            -Transaction.amount,
                        ),
                        else_=0,
                    )
                ),
                0,
            )
        ).where(
            Transaction.user_id == user_id,
            Transaction.deleted_at.is_(None),
        )

        return db.execute(
            statement
        ).scalar_one()

    @staticmethod
    def calculate_credit_card_movement(
        db: Session,
        account_id: UUID,
        user_id: UUID,
    ):
        statement = select(
            func.coalesce(
                func.sum(
                    case(
                        # Credit-card expense increases outstanding liability
                        (
                            (
                                Transaction.source_account_id == account_id
                            )
                            & (
                                Transaction.type
                                == TransactionType.EXPENSE
                            ),
                            Transaction.amount,
                        ),

                        # Payment to credit card reduces outstanding liability
                        (
                            (
                                Transaction.destination_account_id
                                == account_id
                            )
                            & (
                                Transaction.type
                                == TransactionType.TRANSFER
                            ),
                            -Transaction.amount,
                        ),

                        # Refund to credit card reduces outstanding liability
                        (
                            (
                                Transaction.destination_account_id
                                == account_id
                            )
                            & (
                                Transaction.type
                                == TransactionType.REFUND
                            ),
                            -Transaction.amount,
                        ),

                        else_=0,
                    )
                ),
                0,
            )
        ).where(
            Transaction.user_id == user_id,
            Transaction.deleted_at.is_(None),
        )

        return db.execute(
            statement
        ).scalar_one()