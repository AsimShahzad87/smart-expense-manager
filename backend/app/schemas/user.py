from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=150)
    default_currency: str = Field(default="PKR", min_length=3, max_length=3)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    default_currency: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )