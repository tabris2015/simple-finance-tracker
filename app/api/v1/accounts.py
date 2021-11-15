from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore import Client
from app.database.firestore_session import get_session
from app import crud, schemas
from app.models.account import Account, AccountCreate, AccountUpdate

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


@router.put("", response_model=Account)
def update_account(*, db: Client = Depends(get_session), account_in: AccountUpdate):
    account = crud.account.get(db, model_id=account_in.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")

    account = crud.account.update(db, db_obj=account, obj_in=account_in)
    return account


@router.delete("", response_model=schemas.Message)
def delete_account(*, db: Client = Depends(get_session), id: str):
    account = crud.account.get(db, model_id=id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")

    crud.account.remove(db, model_id=id)
    return schemas.Message(message=f"Account with ID={id} deleted.")
