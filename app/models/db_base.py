from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TimestampDBBase(BaseModel):
    """Base model with timestamp for database"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime]


class DBBase(TimestampDBBase):
    """Default database fields"""
    id: UUID = Field(default_factory=uuid4)
