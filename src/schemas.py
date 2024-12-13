from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from src.database.models import UserRole


class ContactBase(BaseModel):
    first_name: str = Field(max_length=128)
    last_name: str = Field(max_length=128)
    email: str = Field(max_length=128)
    phone: str = Field(max_length=128)
    birthday: Optional[date]
    additional_info: Optional[str] = Field(max_length=256)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(max_length=128)
    last_name: Optional[str] = Field(max_length=128)
    email: Optional[EmailStr] = Field(max_length=128)
    phone: Optional[str] = Field(max_length=128)
    birthday: Optional[date]
    additional_info: Optional[str] = Field(max_length=256)


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ContactPhoneUpdate(BaseModel):
    phone: str = Field(..., max_length=128, description="New phone number")


class ContactEmailUpdate(BaseModel):
    email: EmailStr = Field(..., description="New email")


class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr
