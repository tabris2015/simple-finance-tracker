from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore import Client
from app.database.firestore_session import get_session
from app import crud, schemas
from app.models.entry import Entry, EntryCreate, EntryUpdate

router = APIRouter()


@router.get("", response_model=List[Entry])
def read_entries(db: Client = Depends(get_session)):
    entries = crud.entry.get_multi(db)
    return entries


@router.get("/{id}", response_model=Entry)
def read_entry(*, db: Client = Depends(get_session), id: str):
    entry = crud.entry.get(db, model_id=id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry doesn't exist")
    return entry


@router.post("", response_model=Entry)
def create_entry(*, db: Client = Depends(get_session), entry_in: EntryCreate):
    account = crud.account.get(db, model_id=entry_in.account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")

    entry = crud.entry.create(db, obj_in=entry_in)
    return entry


@router.put("", response_model=Entry)
def update_entry(*, db: Client = Depends(get_session), entry_in: EntryUpdate):
    account = crud.account.get(db, model_id=entry_in.account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account doesn't exist")

    entry = crud.entry.get(db, model_id=entry_in.id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry doesn't exist")

    entry = crud.entry.update(db, db_obj=entry, obj_in=entry_in)
    return entry


@router.delete("", response_model=schemas.Message)
def delete_entry(*, db: Client = Depends(get_session), id: str):
    entry = crud.entry.get(db, model_id=id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry doesn't exist")

    crud.entry.remove(db, model_id=id)
    return schemas.Message(message=f"Entry with ID={id} deleted.")
