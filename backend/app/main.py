from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine

from app.api.v1.auth import router as auth_router
from app.api.v1.accounts import router as accounts_router
from app.api.v1.categories import router as categories_router
from app.api.v1.transactions import router as transactions_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Smart Expense Manager",
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)


app.include_router(
    accounts_router,
    prefix="/api/v1",
)


app.include_router(
    categories_router,
    prefix="/api/v1",
)


app.include_router(
    transactions_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Smart Expense Manager API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "UP",
        "database": "CONNECTED"
    }


    @staticmethod
    def update_transaction(
        db: Session,
        current_user: User,
        transaction_id: UUID,
        request: TransactionUpdate,
    ) -> Transaction:

        transaction = TransactionService.get_transaction(
            db,
            current_user,
            transaction_id,
        )

        update_data = request.model_dump(
            exclude_unset=True
        )

        transaction_type = update_data.get(
            "type",
            transaction.type,
        )

        source_account_id = update_data.get(
            "source_account_id",
            transaction.source_account_id,
        )

        destination_account_id = update_data.get(
            "destination_account_id",
            transaction.destination_account_id,
        )

        category_id = update_data.get(
            "category_id",
            transaction.category_id,
        )

        currency = update_data.get(
            "currency",
            transaction.currency,
        ).upper()

        source_account = TransactionService._get_account(
            db,
            current_user,
            source_account_id,
        )

        destination_account = TransactionService._get_account(
            db,
            current_user,
            destination_account_id,
        )

        category = TransactionService._get_category(
            db,
            current_user,
            category_id,
        )

        TransactionService._validate_transaction(
            transaction_type,
            source_account,
            destination_account,
            category,
            currency,
        )

        for field, value in update_data.items():
            if field == "currency" and value is not None:
                value = value.upper()

            if field in (
                "merchant",
                "description",
            ) and value is not None:
                value = value.strip()

            setattr(
                transaction,
                field,
                value,
            )

        return TransactionRepository.save(
            db,
            transaction,
        )


    @staticmethod
    def delete_transaction(
        db: Session,
        current_user: User,
        transaction_id: UUID,
    ) -> Transaction:

        transaction = TransactionService.get_transaction(
            db,
            current_user,
            transaction_id,
        )

        transaction.deleted_at = datetime.now(
            timezone.utc
        )

        return TransactionRepository.save(
            db,
            transaction,
        )