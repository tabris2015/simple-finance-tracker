from fastapi import APIRouter
from app.api.v1 import accounts, entries

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(entries.router, prefix="/entries", tags=["entries"])
