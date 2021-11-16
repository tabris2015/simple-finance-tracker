from typing import TypeVar, Type
from app.crud.base import CRUDBase, ModelType
from app.models.entry import Entry, EntryCreate, EntryUpdate

EntryModelType = TypeVar("EntryModelType", bound=Entry)


class EntryCRUD(CRUDBase[Entry, EntryCreate, EntryUpdate]):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model, "entries")


entry = EntryCRUD(Entry)
