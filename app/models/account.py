from typing import Optional
from enum import Enum
from pydantic import BaseModel
from app.models.db_base import TimestampDBBase


class AccountTypeEnum(str, Enum):
    emergency = "emergency"
    savings = "savings"
    safi = "safi"
    proxy = "proxy"


class CurrencyEnum(str, Enum):
    bs = "BS"
    us = "US"


class AccountBase(BaseModel):
    id: str
    name: str
    description: Optional[str]
    bank: str
    number: int
    currency: CurrencyEnum = CurrencyEnum.bs
    type: AccountTypeEnum = AccountTypeEnum.savings


class Account(AccountBase, TimestampDBBase):
    pass


class AccountCreate(AccountBase, TimestampDBBase):
    id: Optional[str]


class AccountUpdate(AccountBase):
    id: str
    name: Optional[str]
    description: Optional[str]
    bank: Optional[str]
    number: Optional[int]
    currency: Optional[CurrencyEnum]
    type: Optional[AccountTypeEnum]
