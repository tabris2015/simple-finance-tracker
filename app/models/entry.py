from typing import Optional
from pydantic import BaseModel
from app.models.db_base import TimestampDBBase


class EntryBase(TimestampDBBase):
    account_id: str
    balance: int


class Entry(EntryBase):
    pass


class EntryCreate(EntryBase):
    pass


class EntryUpdate(BaseModel):
    account_id: Optional[str]
    balance: Optional[int]
