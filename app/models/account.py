from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.db_base import TimestampDBBase


class AccountBase(BaseModel):
    id: str
    name: str
    description: Optional[str]
    bank: str
    type: str


class Account(AccountBase, TimestampDBBase):
    pass


class AccountCreate(AccountBase, TimestampDBBase):
    id: Optional[str]


class AccountUpdate(AccountBase):
    id: str
    name: Optional[str]
    description: Optional[str]
    bank: Optional[str]
    type: Optional[str]
