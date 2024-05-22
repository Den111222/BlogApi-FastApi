from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def _validate(cls, value: str) -> str:
        if not value:
            return value
        return super()._validate(value)


class BaseUser(BaseModel):
    login: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str


class LoginUser(BaseModel):
    login: str
    password: str


class User(BaseUser):
    id: UUID
    is_superuser: bool = False
    is_deleted: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPayload(User):
    exp: datetime
    user_roles: list[str] = []
    service_name: str = Field(default="auth_service")
