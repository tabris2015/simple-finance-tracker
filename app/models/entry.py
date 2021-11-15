from pydantic import BaseModel
from app.models.account import Account
from app.models.db_base import DBBase


class EntryBase(BaseModel):
    account: Account
    balance: int


class Entry(EntryBase):
    pass


class EntryCreate(EntryBase, DBBase):
    pass

