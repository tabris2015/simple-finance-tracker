from typing import Any, List, TypeVar, Type
from google.cloud.firestore import Client
from app.crud.base import CRUDBase, ModelType
from app.models.account import Account, AccountCreate, AccountUpdate

AccountModelType = TypeVar("AccountModelType", bound=Account)


class AccountCRUD(CRUDBase[Account, AccountCreate, AccountUpdate]):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model, "accounts")


account = AccountCRUD(Account)
