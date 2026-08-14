from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.enums import CategoryType


class CategoryRepository:

    @staticmethod
    def create(
        db: Session,
        category: Category,
    ) -> Category:

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def get_available_categories(
        db: Session,
        user_id: UUID,
    ) -> list[Category]:

        statement = (
            select(Category)
            .where(
                Category.is_active.is_(True),
                or_(
                    Category.is_system.is_(True),
                    Category.user_id == user_id,
                ),
            )
            .order_by(
                Category.category_type,
                Category.name,
            )
        )

        return list(
            db.execute(statement)
            .scalars()
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: UUID,
        user_id: UUID,
    ) -> Category | None:

        statement = select(Category).where(
            Category.id == category_id,
            or_(
                Category.is_system.is_(True),
                Category.user_id == user_id,
            ),
        )

        return db.execute(
            statement
        ).scalar_one_or_none()

    @staticmethod
    def get_available_category_by_name_and_type(
        db: Session,
        user_id: UUID,
        name: str,
        category_type: CategoryType,
    ) -> Category | None:

        statement = select(Category).where(
            or_(
                Category.is_system.is_(True),
                Category.user_id == user_id,
            ),
            Category.name.ilike(name.strip()),
            Category.category_type == category_type,
        )

        return db.execute(
            statement
        ).scalars().first()

    @staticmethod
    def get_user_category_by_name(
        db: Session,
        user_id: UUID,
        name: str,
    ) -> Category | None:

        statement = select(Category).where(
            Category.user_id == user_id,
            Category.name.ilike(name.strip()),
        )

        return db.execute(
            statement
        ).scalars().first()

    @staticmethod
    def save(
        db: Session,
        category: Category,
    ) -> Category:

        db.add(category)
        db.commit()
        db.refresh(category)

        return category