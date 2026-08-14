from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

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