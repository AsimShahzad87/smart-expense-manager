from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def create_category(
        db: Session,
        current_user: User,
        request: CategoryCreate,
    ) -> Category:

        name = request.name.strip()

        existing_category = (
            CategoryRepository.get_user_category_by_name(
                db,
                current_user.id,
                name,
            )
        )

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A category with this name already exists",
            )

        category = Category(
            user_id=current_user.id,
            name=name,
            category_type=request.category_type,
            icon=request.icon,
            is_system=False,
            is_active=True,
        )

        return CategoryRepository.create(
            db,
            category,
        )

    @staticmethod
    def get_categories(
        db: Session,
        current_user: User,
    ) -> list[Category]:

        return CategoryRepository.get_available_categories(
            db,
            current_user.id,
        )

    @staticmethod
    def get_category(
        db: Session,
        current_user: User,
        category_id: UUID,
    ) -> Category:

        category = CategoryRepository.get_by_id(
            db,
            category_id,
            current_user.id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return category

    @staticmethod
    def update_category(
        db: Session,
        current_user: User,
        category_id: UUID,
        request: CategoryUpdate,
    ) -> Category:

        category = CategoryService.get_category(
            db,
            current_user,
            category_id,
        )

        if category.is_system:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="System categories cannot be modified",
            )

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            new_name = update_data["name"].strip()

            existing_category = (
                CategoryRepository.get_user_category_by_name(
                    db,
                    current_user.id,
                    new_name,
                )
            )

            if (
                existing_category is not None
                and existing_category.id != category.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A category with this name already exists",
                )

            update_data["name"] = new_name

        for field, value in update_data.items():
            setattr(
                category,
                field,
                value,
            )

        return CategoryRepository.save(
            db,
            category,
        )

    @staticmethod
    def deactivate_category(
        db: Session,
        current_user: User,
        category_id: UUID,
    ) -> Category:

        category = CategoryService.get_category(
            db,
            current_user,
            category_id,
        )

        if category.is_system:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="System categories cannot be deactivated",
            )

        category.is_active = False

        return CategoryRepository.save(
            db,
            category,
        )