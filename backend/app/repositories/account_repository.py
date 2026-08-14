from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:

    @staticmethod
    def create(
        db: Session,
        account: Account,
    ) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: UUID,
    ) -> list[Account]:
        statement = (
            select(Account)
            .where(Account.user_id == user_id)
            .order_by(Account.created_at.desc())
        )

        return list(
            db.execute(statement).scalars().all()
        )

    @staticmethod
    def get_by_id_and_user(
        db: Session,
        account_id: UUID,
        user_id: UUID,
    ) -> Account | None:
        statement = select(Account).where(
            Account.id == account_id,
            Account.user_id == user_id,
        )

        return db.execute(
            statement
        ).scalar_one_or_none()

    @staticmethod
    def save(
        db: Session,
        account: Account,
    ) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)

        return account