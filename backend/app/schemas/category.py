from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CategoryType


class CategoryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    category_type: CategoryType

    icon: str | None = Field(
        default=None,
        max_length=100,
    )


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    category_type: CategoryType | None = None

    icon: str | None = Field(
        default=None,
        max_length=100,
    )

    is_active: bool | None = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    category_type: CategoryType
    icon: str | None
    is_system: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )