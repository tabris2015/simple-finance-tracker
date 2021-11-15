from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime
from pydantic import BaseModel
from google.cloud.firestore import Client

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)
UpdateModelType = TypeVar("UpdateModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, model: Type[ModelType], collection_name: str):
        self.model = model
        self.collection_name = collection_name

    def get(self, db: Client, model_id: Any) -> Optional[ModelType]:
        doc_ref = db.collection(self.collection_name).document(model_id)
        doc = doc_ref.get()

        return self.model(id=doc.id, **doc.to_dict())

    def get_multi(self, db: Client) -> List[ModelType]:
        obj_list = []

        for doc in db.collection(self.collection_name).stream():
            obj_list.append(self.model(id=doc.id, **doc.to_dict()))

        return obj_list

    def create(self, db: Client, *, obj_in: CreateModelType) -> ModelType:
        data = obj_in.dict(exclude={"id"})
        _, doc_ref = db.collection(self.collection_name).add(data)
        doc = doc_ref.get()
        if doc.exists:
            return self.model(id=doc.id, **doc.to_dict())

    def update(self, db: Client, *, db_obj: ModelType, obj_in: Union[UpdateModelType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_none=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        doc_ref = db.collection(self.collection_name).document(update_data["id"])
        doc_ref.update({key: value for key, value in update_data.items() if key != "id"})
        doc = doc_ref.get()
        return self.model(id=doc.id, **doc.to_dict())

    def remove(self, db: Client, *, model_id: Any) -> ModelType:
        # soft deletes
        return self.update(db, db_obj=self.get(db, model_id), obj_in={"id": model_id, "deleted_at": datetime.utcnow()})
