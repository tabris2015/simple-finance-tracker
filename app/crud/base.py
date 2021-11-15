from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
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

    def update(self):
        pass

    def remove(self):
        pass
