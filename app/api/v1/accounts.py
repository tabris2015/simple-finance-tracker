from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore import Client
from app.database.firestore_session import get_session
from app import crud
from app.models.account import Account, AccountCreate

router = APIRouter()


@router.get("", response_model=List[Account])
def read_accounts(db: Client = Depends(get_session)):
    accounts = crud.account.get_multi(db)
    return accounts


@router.get("/{id}", response_model=Account)
def read_account(*, db: Client = Depends(get_session), id: str):
    account = crud.account.get(db, model_id=id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")
    return account


@router.post("", response_model=Account)
def create_account(*, db: Client = Depends(get_session), account_in: AccountCreate):
    account = crud.account.create(db, obj_in=account_in)
    return account
